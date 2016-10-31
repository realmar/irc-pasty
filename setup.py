#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name = "irc-pasty",
    version = "1",
    packages = find_packages(),
    test_suite = 'nose.collector'
)
