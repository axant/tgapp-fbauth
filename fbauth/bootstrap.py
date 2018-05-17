# -*- coding: utf-8 -*-
"""Setup the fbauth application"""

from fbauth import model
from tgext.pluggable import app_model

import logging


log = logging.getLogger(__name__)


def bootstrap(command, conf, vars):
    log.info('Bootstrapping fbauth...')
