# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-fbauth."""

from tg import request
from markupsafe import Markup
from urllib import quote_plus

def _fb_init(appid, html, script):
    if appid:
        html += '<div id="fb-root"></div>'
        script += '''<script type="text/javascript">
        window.fbAsyncInit = function() {
            FB.init({appId      : "%(appid)s",
                     status     : false,
                     cookie     : true,
                     xfbml      : true,
                     oauth      : true});
        };
        (function() {
          var e = document.createElement('script'); e.async = true;
          e.src = document.location.protocol +
            '//connect.facebook.net/en_US/all.js';
          document.getElementById('fb-root').appendChild(e);
        }());
        </script>''' % dict(appid=appid)

    return html, script

def login_button(appid, text='Login with Facebook', scope=None, remember=''):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button" data-width="100" scope="%(scope)s" onlogin="fbauth_login()">
                %(text)s
              </div>''' % dict(text=text, scope=scope)

    script = '''<script>
function fbauth_login() {
    var fbanswer = FB.getAuthResponse();
    if (fbanswer['accessToken']) {
        var remember = "%(remember)s";
        var expiry = fbanswer['expiresIn'];
        var access_token = fbanswer['accessToken'];
        var loginUrl = "/fbauth/login/" + access_token + "/" + expiry + "?came_from=%(came_from)s";
        if (remember)
            loginUrl += '&remember=' + remember;
        window.location = loginUrl;
    }
}
</script>''' % dict(remember=remember, came_from=quote_plus(request.url))

    html, script = _fb_init(appid, html, script)
    return Markup(html + script)

def register_button(appid, text='Register with Facebook', scope=None, remember=''):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button" scope="%(scope)s" onlogin="fbauth_register()">
                %(text)s
              </div>''' % dict(text=text, scope=scope)

    script = '''<script>
function fbauth_register() {
    var fbanswer = FB.getAuthResponse();
    if (fbanswer['accessToken']) {
        var remember = "%(remember)s";
        var expiry = fbanswer['expiresIn'];
        var access_token = fbanswer['accessToken'];
        var loginUrl = "/fbauth/register/" + access_token + "/" + expiry + "?came_from=%(came_from)s";
        if (remember)
            loginUrl += '&remember=' + remember;
        window.location = loginUrl;
    }
}
</script>''' % dict(remember=remember, came_from=quote_plus(request.url))

    html, script = _fb_init(appid, html, script)
    return Markup(html + script)

def connect_button(appid, text='Connect your Facebook account', scope=None):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button" scope="%(scope)s" onlogin="fbauth_connect()">
                %(text)s
              </div>''' % dict(text=text, scope=scope)

    script = '''<script>
function fbauth_connect() {
    var fbanswer = FB.getAuthResponse();
    if (fbanswer['accessToken']) {
        var expiry = fbanswer['expiresIn'];
        var access_token = fbanswer['accessToken'];
        var loginUrl = "/fbauth/connect/" + access_token + "/" + expiry + "?came_from=%(came_from)s";
        window.location = loginUrl;
    }
}
</script>''' % dict(came_from=quote_plus(request.url))

    html, script = _fb_init(appid, html, script)
    return Markup(html + script)