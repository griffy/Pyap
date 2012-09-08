#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Pyap',
      version='0.1.1',
      description='Python Audio Player Library',
      author='Joel Griffith',
      packages=find_packages(),
      requires=['mutagen', 'pygst', 'sqlalchemy']
)
