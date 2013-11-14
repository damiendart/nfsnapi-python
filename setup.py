from distutils.core import setup
import nfsnapi

setup(
  name = "nfsnapi",
  version = nfsnapi.__version__,
  long_description = open("readme.txt").read(),
  author = "Damien Dart",
  author_email = "damiendart@pobox.com",
  url = "https://github.com/damiendart/nfsnapi-python",
  py_modules = ["nfsnapi"]
)
