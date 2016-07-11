#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lena
----------------------------------

Tests for `lena` module.
"""

import unittest

import lena


class TestLena(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        assert(lena.hello_world())
        pass

    def tearDown(self):
        pass
