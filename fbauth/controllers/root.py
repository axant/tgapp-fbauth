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

        fb_user = model.FBAuthInfo.user_by_facebook_id(facebook_id)

        if not fb_user:
            flash(_('Unable to find an user for the specified facebook token'), 'error')
            return redirect_on_fail()

        login_user(fb_user.user.user_name, remember)
        hooks.notify('fbauth.on_login', args=(answer, fb_user))

        if has_fbtoken_expired(fb_user):
            fb_user.access_token = token
            fb_user.access_token_expiry = expiry

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

        fb_user = model.FBAuthInfo.user_by_facebook_id(facebook_id)

        if fb_user:
            #If the user already exists, just login him.
            login_user(fb_user.user.user_name, remember)
            if has_fbtoken_expired(fb_user):
                fb_user.access_token = token
                fb_user.access_token_expiry = expiry

            hooks.notify('fbauth.on_login', args=(answer, fb_user))
            redirect_to = add_param_to_query_string(config.sa_auth['post_login_url'], 'came_from', came_from)
            return redirect(redirect_to)

        user_dict = dict(
            user_name='fb:%s' % facebook_id,
            display_name=answer.get('name', answer.get('username', answer.get('first_name', 'Anonymous'))),
            email_address=answer.get('email', '%s@facebook.com' % answer.get('username', facebook_id)),
            password=token
        )
        hooks.notify('fbauth.on_registration', args=(answer, user_dict))

        u = model.provider.create(app_model.User, user_dict)

        fbi_dict = dict(
            user=u,
            facebook_id=facebook_id,
            registered=True,
            just_connected=True,
            access_token=token,
            access_token_expiry=expiry,
            profile_picture='http://graph.facebook.com/v2.3/%s/picture' % facebook_id
        )
        fbi_user = model.provider.create(model.FBAuthInfo, fbi_dict)

        login_user(u.user_name, remember)
        if has_fbtoken_expired(fbi_user):
            fbi_user.access_token = token
            fbi_user.access_token_expiry = expiry

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

        fb_user = model.FBAuthInfo.user_by_facebook_id(facebook_id)
        if fb_user:
            flash(_('An user for this facebook token is already registered'), 'error')
            return redirect(came_from)

        u = request.identity['user']
        fbi_dict = dict(
            user=u,
            facebook_id=facebook_id,
            registered=False,
            just_connected=True,
            access_token=token,
            access_token_expiry=expiry,
            profile_picture='http://graph.facebook.com/v2.3/%s/picture' % facebook_id
        )

        model.provider.create(model.FBAuthInfo, fbi_dict)

        return redirect(came_from)
