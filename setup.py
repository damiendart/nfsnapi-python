from distutils.core import setup
import nfsnapi

setup(
  name = "nfsnapi",
  version = nfsnapi.__version__,
  # FIXME: Change description.
  description = "An unofficial NearlyFreeSpeech.NET API thing.",
  long_description = open("readme.txt").read(),
  author = "Damien Dart",
  author_email = "damiendart@pobox.com",
  url = "https://github.com/damiendart/nfsnapi-python",
  py_modules = ["nfsnapi"],
  classifiers = (
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: Public Domain",
    "Programming Language :: Python",
    # TODO: Test "nfsnapi" with other versions of Python.
    "Programming Language :: Python :: 2.7",
    "Operating System :: OS Independent",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules"
  )
)
