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
                     oauth      : true,
                     version    : 'v2.10'});
        };
        (function() {
          var e = document.createElement('script'); e.async = true;
          e.src = document.location.protocol +
            '//connect.facebook.net/en_US/all.js';
          document.getElementById('fb-root').appendChild(e);
        }());
        </script>''' % dict(appid=appid)

    return html, script


def login_button(appid, text='Login with Facebook', scope=None, remember='', size='medium'):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button" scope="%(scope)s" size="%(size)s" onlogin="fbauth_login()">
                %(text)s
              </div>''' % dict(text=text, scope=scope, size=size)

    script = fbauth_javascript_function_for_base_facebook_login(remember, request)
    html, script = _fb_init(appid, html, script)
    return Markup(html + script)


def login_button_custom(appid, text='Login with Facebook', scope=None, remember='', img_btn=''):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button">
                <a href="#" id="facebook-login-btn" onclick="custom_facebook_login();"><img id="fb-login-image-custom" src="%(img_btn)s" alt="%(text)s" class="share-button"/></a>
              </div>''' % dict(img_btn=img_btn, text=text)

    script = fbauth_javascript_function_for_base_facebook_login(remember, request) + fbauth_javascript_function_for_custom_facebook_login(scope)
    html, script = _fb_init(appid, html, script)
    return Markup(html + script)


def register_button(appid, text='Register with Facebook', scope=None, remember='', size='medium'):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button" scope="%(scope)s" size="%(size)s" onlogin="fbauth_register()">
                %(text)s
              </div>''' % dict(text=text, scope=scope, size=size)

    script = fbauth_javascript_function_for_base_facebook_registration(remember, request)
    html, script = _fb_init(appid, html, script)
    return Markup(html + script)


def register_button_custom(appid, text='Register with Facebook', scope=None, remember='', img_btn=''):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button">
                <a href="#" id="fb-login-button" onclick="custom_facebook_registration();"><img id="fb-register-image-custom" src="%(img_btn)s" alt="%(text)s" class="share-button"/></a>
              </div>''' % dict(img_btn=img_btn, text=text)

    script = fbauth_javascript_function_for_base_facebook_registration(remember, request) + fbauth_javascript_function_for_custom_facebook_registration(scope)
    html, script = _fb_init(appid, html, script)
    return Markup(html + script)


def connect_button(appid, text='Connect your Facebook account', scope=None, size='medium'):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button" scope="%(scope)s" size="%(size)s" onlogin="fbauth_connect()">
                %(text)s
              </div>''' % dict(text=text, scope=scope, size=size)


    script = fbauth_javascript_function_for_base_facebook_connect(request)
    html, script = _fb_init(appid, html, script)
    return Markup(html + script)


def connect_button_custom(appid, text='Connect your Facebook account', scope=None, img_btn=''):
    if not scope:
        scope = "user_about_me,email"

    html = '''<div class="fb-login-button">
                <a href="#" id="fb-login-button" onclick="custom_facebook_connect();"><img id="fb-connect-image-custom" src="%(img_btn)s" alt="%(text)s" class="share-button"/></a>
              </div>''' % dict(img_btn=img_btn, text=text)

    script = fbauth_javascript_function_for_base_facebook_connect(request) + fbauth_javascript_function_for_custom_facebook_connect(scope)

    html, script = _fb_init(appid, html, script)
    return Markup(html + script)


#  LOGIN JAVASCRIPT FUNCTION
def fbauth_javascript_function_for_base_facebook_login(remember, request):
    return '''<script type="text/javascript">
        function fbauth_login(fbanswer) {
            if (typeof fbanswer === "undefined")
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
    </script>''' % dict(remember=remember, came_from=encode_url(request.GET.get('came_from', '/')))


def fbauth_javascript_function_for_custom_facebook_login(scope):
    return '''<script type="text/javascript">
        function custom_facebook_login() {
            FB.login(function (response_login) {
                fbauth_login(response_login['authResponse']);
            }, {
                scope: '%(scope)s',
                return_scopes: true
            });
        }
    </script>''' % dict(scope=scope)


#  REGISTRATION JAVASCRIPT FUNCTION
def fbauth_javascript_function_for_base_facebook_registration(remember, request):
    return '''<script type="text/javascript">
function fbauth_register(fbanswer) {
    if (typeof fbanswer === "undefined")
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
</script>''' % dict(remember=remember, came_from=encode_url(request.GET.get('came_from', '/')))


def fbauth_javascript_function_for_custom_facebook_registration(scope):
    return '''<script type="text/javascript">
        function custom_facebook_registration() {
            FB.login(function (response_login) {
                fbauth_register(response_login['authResponse']);
            }, {
                scope: '%(scope)s',
                return_scopes: true
            });
        }
    </script>''' % dict(scope=scope)


#  CONNECT JAVASCRIPT FUNCTION
def fbauth_javascript_function_for_base_facebook_connect(request):
    return '''<script type="text/javascript">
function fbauth_connect(fbanswer) {
    if (typeof fbanswer === "undefined")
        var fbanswer = FB.getAuthResponse();
    if (fbanswer['accessToken']) {
        var expiry = fbanswer['expiresIn'];
        var access_token = fbanswer['accessToken'];
        var loginUrl = "/fbauth/connect/" + access_token + "/" + expiry + "?came_from=%(came_from)s";
        window.location = loginUrl;
    }
}
</script>''' % dict(came_from=encode_url(request.GET.get('came_from', '/')))


def fbauth_javascript_function_for_custom_facebook_connect(scope):
    return '''<script type="text/javascript">
        function custom_facebook_connect() {
                FB.login(function (response_login) {
                fbauth_connect(response_login['authResponse']);
            }, {
                scope: '%(scope)s',
                return_scopes: true
            });
        }
    </script>''' % dict(scope=scope)


def encode_url(url):
    try:
        from urllib.parse import quote
    except ImportError:
        from urllib import quote
    return quote(url, safe='')
