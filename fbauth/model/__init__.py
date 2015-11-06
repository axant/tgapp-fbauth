# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession, app_model

log = logging.getLogger('tgapp-fbauth')

DBSession = PluggableSession()
FBAuthInfo = None


def init_model(app_session):
    DBSession.configure(app_session)


def import_models():
    global FBAuthInfo
    if tg.config.get('use_sqlalchemy', False):
        from .sqla_models import FBAuthInfo
    elif tg.config.get('use_ming', False):
        from .ming_models import FBAuthInfo
        app_model.User.fbauth = property(
            lambda o: FBAuthInfo.fbauth_user(o._id)
        )


class PluggableSproxProvider(object):
    def __init__(self):
        self._provider = None

    def _configure_provider(self):
        if tg.config.get('use_sqlalchemy', False):
            log.info('Configuring FBAuth for SQLAlchemy')
            from sprox.sa.provider import SAORMProvider
            self._provider = SAORMProvider(session=DBSession)
        elif tg.config.get('use_ming', False):
            log.info('Configuring FBAuth for Ming')
            from sprox.mg.provider import MingProvider
            self._provider = MingProvider(DBSession)
        else:
            raise ValueError('FBAuth should be used with sqlalchemy or ming')

    def __getattr__(self, item):
        if self._provider is None:
            self._configure_provider()

        return getattr(self._provider, item)

provider = PluggableSproxProvider()
