#!/usr/bin/env python
#coding: utf-8
from distutils.core import setup

import sys
import os
reload(sys).setdefaultencoding("UTF-8")

def get_long_desc():
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(setup_dir, 'README.md')
    return open(filename).read().decode('utf8')

setup(
    name='django-onpay',
    version='0.1',
    author='Denis Buriy',
    author_email='denger@footter.com',

    packages=['onpay'],

    url='http://bitbucket.org/denger/django-onpay/',
    download_url = 'http://bitbucket.org/denger/django-onpay/get/tip.zip',
    license = 'MIT license',
    description = u'Приложение для интеграции платежной системы ONPAY в проекты на Django.'.encode('utf8'),
    long_description = get_long_desc(),

    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
)
