# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config, require, \
    hooks
from tg.i18n import ugettext as _, lazy_ugettext as l_

try:
    from tg.predicates import not_anonymous
except ImportError:
    from repoze.what.predicates import not_anonymous

from tgext.pluggable import app_model

from fbauth import model
from fbauth.model import DBSession
from fbauth.lib.utils import (login_user, has_fbtoken_expired, validate_token,
                              add_param_to_query_string, redirect_on_fail)

import json
from urllib import urlopen

class RootController(TGController):
    @expose()
    def login(self, token, expiry, came_from=None, remember=None):
        token, expiry = validate_token(token, expiry)

        fbanswer = urlopen('https://graph.facebook.com/v2.3/me?access_token=%s' % token)
        try:
            answer = json.loads(fbanswer.read())
            facebook_id = answer['id']
        except:
            flash(_('Fatal error while trying to contact Facebook'), 'error')
            return redirect_on_fail()
        finally:
            fbanswer.close()

        user = model.FBAuthInfo.user_by_facebook_id(facebook_id)
        if not user:
            flash(_('Unable to find an user for the specified facebook token'), 'error')
            return redirect_on_fail()

        login_user(user.user_name, remember)
        hooks.notify('fbauth.on_login', args=(answer, user))

        if has_fbtoken_expired(user):
            user.fbauth.access_token = token
            user.fbauth.access_token_expiry = expiry

        redirect_to = add_param_to_query_string(config.sa_auth['post_login_url'], 'came_from', came_from)
        return redirect(redirect_to)

    @expose()
    def register(self, token, expiry, came_from=None, remember=None):
        token, expiry = validate_token(token, expiry)

        fbanswer = urlopen('https://graph.facebook.com/v2.3/me?access_token=%s' % token)
        try:
            answer = json.loads(fbanswer.read())
            facebook_id = answer['id']
        except:
            flash(_('Fatal error while trying to contact Facebook'), 'error')
            return redirect_on_fail()
        finally:
            fbanswer.close()

        user = model.FBAuthInfo.user_by_facebook_id(facebook_id)
        if user:
            #If the user already exists, just login him.
            login_user(user.user_name, remember)
            if has_fbtoken_expired(user):
                user.fbauth.access_token = token
                user.fbauth.access_token_expiry = expiry

            hooks.notify('fbauth.on_login', args=(answer, user))
            redirect_to = add_param_to_query_string(config.sa_auth['post_login_url'], 'came_from', came_from)
            return redirect(redirect_to)

        u = app_model.User(user_name='fb:%s' % facebook_id,
                           display_name=answer.get('name',
                                                   answer.get('username',
                                                              answer.get('first_name', 'Anonymous'))),
                           email_address=answer.get('email', '%s@facebook.com' % answer.get('username',
                                                                                            facebook_id)),
                           password=token)
        DBSession.add(u)
        hooks.notify('fbauth.on_registration', args=(answer, u))

        fbi = model.FBAuthInfo(user=u, facebook_id=facebook_id, registered=True, just_connected=True,
                               access_token=token, access_token_expiry=expiry,
                               profile_picture='http://graph.facebook.com/v2.3/%s/picture' % facebook_id)
        DBSession.add(fbi)

        login_user(u.user_name, remember)
        if has_fbtoken_expired(u):
            u.fbauth.access_token = token
            u.fbauth.access_token_expiry = expiry

        redirect_to = add_param_to_query_string(config.sa_auth['post_login_url'], 'came_from', came_from)
        return redirect(redirect_to)

    @expose()
    @require(not_anonymous())
    def connect(self, token, expiry, came_from=None):
        if not came_from:
            came_from = request.referer or config.sa_auth['post_login_url']

        token, expiry = validate_token(token, expiry)

        fbanswer = urlopen('https://graph.facebook.com/v2.3/me?access_token=%s' % token)
        try:
            answer = json.loads(fbanswer.read())
            facebook_id = answer['id']
        except:
            flash(_('Fatal error while trying to contact Facebook'), 'error')
            return redirect_on_fail()
        finally:
            fbanswer.close()

        user = model.FBAuthInfo.user_by_facebook_id(facebook_id)
        if user:
            flash(_('An user for this facebook token is already registered'), 'error')
            return redirect(came_from)

        u = request.identity['user']
        fbi = model.FBAuthInfo(user=u, facebook_id=facebook_id, registered=False, just_connected=True,
                               access_token=token, access_token_expiry=expiry,
                               profile_picture='http://graph.facebook.com/v2.3/%s/picture' % facebook_id)
        DBSession.add(fbi)
        return redirect(came_from)

