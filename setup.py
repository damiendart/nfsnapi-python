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
    "Operating System :: OS Independent",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ),
  description = nfsnapi.__doc__.split("\n", 1)[0],
  keywords = "nearlyfreespeech nfsn",
  long_description = open("readme.txt").read(),
  name = "nfsnapi",
  py_modules = ["nfsnapi"],
  url = "https://github.com/damiendart/nfsnapi-python",
  version = nfsnapi.__version__
)
