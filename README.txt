=======
nfsnapi
=======

A simple Python package with a couple of functions (and an exception
class) that make working with the `NearlyFreeSpeech.NET API`_ easier.

.. _NearlyFreeSpeech.NET API: https://members.nearlyfreespeech.net/wiki/API


Synopsis
--------

.. code-block:: pycon

  >>> import nfsnapi
  >>> # Replace USERNAME, API_KEY, and so on with actual values.
  >>> nfsnapi.run_request("USERNAME", "API_KEY",
  ... "/account/ACCOUNT_NUMBER/balance")
  '10.56'
  >>> nfsnapi.run_request("USERNAME", "API_KEY",
  ... "/dns/DOMAIN/listRRs", "type=A")
  (A bunch of JSON not shown.)
  >>> # And so on...


Licence
-------

"nfsnapi" was written by Damien Dart, <damiendart@pobox.com>. This is
free and unencumbered software released into the public domain. For more
information, please refer to the accompanying "UNLICENCE" file.
