About FBAuth
-------------------------

fbauth is a Pluggable Facebook Authentication application for TurboGears2.

It aims at making easy to implement authentication and registration with
FaceBook Connect in any TurboGears2 application.

Installing
-------------------------------

fbauth can be installed both from pypi or from bitbucket::

    easy_install tgapp-fbauth

should just work for most of the users

Plugging fbauth
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with fbauth::

    plug(base_config, 'fbauth')

You will be able to add facebook login, registration and connect
buttons using the helpers provided by fbauth.

**Keep in mind that facebook connect won't work correctly with
applications that are not running on port 80**

FaceBook Id and Avatar
-----------------------

When using FBAuth users will have a new related entity called ``fbauth``.
Accessing ``user.fbauth`` it is possible to access the user ``user.fbauth.facebook_id``
and ``user.fbauth.profile_picture``.

FBAuth Helpers
----------------------

fbauth provides a bunch of helpers which will automatically
generate the buttons and the javascript required to let
your users log into your application using FaceBook Connect:

     * **h.fbauth.login_button(appid, text='Login with Facebook', scope=None, remember='')**
        Places a login button.
        Login permits to log with an user that has already been connected with a facebook id.
        To connect an user to a facebook id, *registration* or *connect* can be used.

        The ``appid`` parameter has to be the id of your application, if ``None`` is provided
        the FB.init call will be skipped so that FB can be manually initialized.

        The ``text`` parameter is the text to show inside the button.

        The ``scope`` parameter is the permissions that the application will ask to facebook.
        By default those are only user data and email.

        The ``remember`` parameter can be used to log the user with an expiration date instead
        of using a session cookie, so that the session can last longer than the browser tab life.

     * **h.fbauth.register_button(appid, text='Register with Facebook', scope=None, remember='')**
        Places a registration button.
        Registration automatically creates a new user from its facebook data and logs him in.
        *For registration to work it is required that any additional data apart the data which
        is already required by default in the quickstart User model can be nullable. A way
        to identify newly registered users and ask for missing data is provided*
        If an user for the obtained token already exists that user is logged in instead of
        creating a new user. This permits to implement 1 click registration and login.
        Newly created users will have both ``user.fbauth.registered`` and ``user.fbauth.just_connected``
        flags at ``True`` so that it is possible to identify when users have just registered
        and ask them more informations that facebook didn't provide. It is suggested to set
        the ``just_connected`` flag to ``False`` on post_login handler to correctly track
        users that have just registered for real.

        The ``appid`` parameter has to be the id of your application, if ``None`` is provided
        the FB.init call will be skipped so that FB can be manually initialized.

        The ``text`` parameter is the text to show inside the button.

        The ``scope`` parameter is the permissions that the application will ask to facebook.
        By default those are only user data and email.

        The ``remember`` parameter can be used to log the user with an expiration date instead
        of using a session cookie, so that the session can last longer than the browser tab life.

     * **h.fbauth.connect_button(appid, text='Connect your Facebook account', scope=None)**
        Places a connect account button.
        Connect permits to associate an already existing user to a facebook account so that
        it can later log with its facebook account.
        Newly connected users will have ``user.fbauth.just_connected`` flag at ``True`` while
        the ``user.fbauth.registered`` flag will be ``False`` to differentiate users that
        have been connected from users that have registered with facebook.

        The ``appid`` parameter has to be the id of your application, if ``None`` is provided
        the FB.init call will be skipped so that FB can be manually initialized.

        The ``text`` parameter is the text to show inside the button.

        The ``scope`` parameter is the permissions that the application will ask to facebook.
        By default those are only user data and email.

FBAuth Utilities
------------------

FBAuth provides a bunch of utility methods that make easy to work with facebook:

    * **fbauth.lib.has_fbtoken_expired(user)**
        Checks if the facebook token for the given users has expired or not, this can be
        useful when calling facebook API. The facebook token itself can be retrieved from
        ``user.fbauth.access_token``