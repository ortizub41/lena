# -*- coding: utf-8 -*-
from __future__ import print_function
from ._version import get_versions

__author__ = 'Juan Ortiz'
__email__ = 'ortizub41@gmail.com'
__version__ = get_versions()['version']
del get_versions

def hello_world():
    print('Hello, world!')
    return True
