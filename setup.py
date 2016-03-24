#!/usr/bin/env python

"""Setup script for "nfsnapi".

This file was written by Damien Dart, <damiendart@pobox.com>. This is
free and unencumbered software released into the public domain. For more
information, please refer to the accompanying "UNLICENCE" file.
"""

from distutils.core import setup
import nfsnapi

setup(
  author = "Damien Dart",
  author_email = "damiendart@pobox.com",
  classifiers = (
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: Public Domain",
    "Programming Language :: Python",
    # TODO: Test "nfsnapi" with other versions of Python.
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Operating System :: OS Independent",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ),
  description = nfsnapi.__doc__.split("\n", 1)[0],
  keywords = "nearlyfreespeech nfsn",
  long_description = open("README.txt").read(),
  name = "nfsnapi",
  py_modules = ["nfsnapi"],
  url = "https://www.robotinaponcho.net/git/?p=nfsnapi-python.git",
  version = nfsnapi.__version__
)
