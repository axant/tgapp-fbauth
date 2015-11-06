import tg
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs, urlunparse
from urllib import urlencode

def redirect_on_fail():
    return tg.redirect(tg.request.referer or tg.config.sa_auth['post_logout_url'])

def validate_token(token, expiry):
    if not token or not token.strip():
        tg.flash(_('Missing facebook token'), 'error')
        return redirect_on_fail()

    try:
        expiry = expirydate_from_sec(int(expiry))
    except ValueError:
        tg.flash(_('Invalid Expiry Time for facebook token'), 'error')
        return redirect_on_fail()

    return token, expiry


def login_user(user_name, expire=None):
    request = tg.request
    response = tg.response

    request.cookies.clear()
    authentication_plugins = request.environ['repoze.who.plugins']
    identifier = authentication_plugins['main_identifier']

    login_options = {'repoze.who.userid':user_name}
    if expire:
        login_options['max_age'] = expire

    if not request.environ.get('repoze.who.identity'):
        response.headers = identifier.remember(request.environ, login_options)


def has_fbtoken_expired(user):
    expire = user.access_token_expiry
    if not expire:
        return True

    if datetime.now() > expire:
        return True

    return False


def expirydate_from_sec(seconds):
    seconds -= 3
    if seconds <= 0:
        raise ValueError('Facebook token already expired')

    return datetime.now() + timedelta(seconds=seconds)


def add_param_to_query_string(url, param, value):
    url_parts = list(urlparse(url))
    query_parts = parse_qs(url_parts[4])
    query_parts[param] = value
    url_parts[4] = urlencode(query_parts, doseq=True)
    return urlunparse(url_parts)
