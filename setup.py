# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.1.5",
    "tgext.pluggable"
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-fbauth',
    version='0.0.3',
    description='Facebook Authentication for TurboGears2',
    long_description=README,
    author='Alessandro Molina',
    author_email='alessandro.molina@axant.it',
    url='http://bitbucket.org/_amol_/tgapp-fbauth',
    keywords='turbogears2.application',
    setup_requires=[],
    paster_plugins=[],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'tgapp.fbauth': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    entry_points="""
    """,
    dependency_links=[
        ],
    zip_safe=False
)
