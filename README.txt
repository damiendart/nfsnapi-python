=======
nfsnapi
=======

A simple Python package with a couple of functions (and an exception
class) that make working with the `NearlyFreeSpeech.NET API`_ easier.

.. _NearlyFreeSpeech.NET API: https://members.nearlyfreespeech.net/wiki/API

``nfsnapi`` supports Python 2.7 and later, and Python 3. There are no
prerequisites other than a supported version of Python.


Synopsis
--------

::

  >>> import nfsnapi
  >>> # Replace USERNAME, API_KEY, and so on with actual values.
  >>> nfsnapi.run_request("USERNAME", "API_KEY",
  ... "/account/ACCOUNT_NUMBER/balance")
  u'10.56'
  >>> nfsnapi.run_request("USERNAME", "API_KEY",
  ... "/dns/DOMAIN/listRRs", "type=A")
  (A bunch of JSON not shown.)
  >>> # And so on...


Installation
------------

The usual ``python setup.py install`` dance will install ``nfsnapi``.
Alternatively, ``nfsnapi`` is available from `PyPI`_ via your Python
package manager of choice.

.. _PyPI: https://pypi.python.org/pypi/nfsnapi


Documentation and Testing
-------------------------

The ``nfsnapi`` module is heavily documented. Running
``nfnsapi-tests.py`` will, funnily enough, run some tests; the tests
require a configuration file with API credentials and what-not, see
``nfnsapi-tests.py``'s docstring for more information.

There's support for `Tox`_, which will run the tests on all available
and supported versions of Python.

.. _Tox: https://testrun.org/tox/latest/


Licence
-------

``nfsnapi`` was written by Damien Dart, <damiendart@pobox.com>. This is
free and unencumbered software released into the public domain. For more
information, please refer to the accompanying "UNLICENCE" file.
