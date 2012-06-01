# -*- coding: utf-8 -*-
"""Setup the fbauth application"""

from fbauth import model
from tgext.pluggable import app_model

def bootstrap(command, conf, vars):
    print 'Bootstrapping fbauth...'
