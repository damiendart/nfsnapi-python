#!/usr/bin/env python

"""Tests for the "nfsnapi" module.

These tests do not modify any of your settings. To run these tests you
must have an account with NearlyFreeSpeech.NET, along with:

  - an API key for your account provided by NearlyFreeSpeech.NET and
  - a domain name whose DNS is managed by NearlyFreeSpeech.NET.

Credentials and other required information are read from a
"nfsnapi-tests.cfg" file located either in the current directory or the
home directory of the user running the tests. The contents of the
configuration file must adhere to the following structure:

  [credentials]
  accountnumber = A1B2-C3D4E5F6
  apikey = abcdefgh12345678
  username = testuser
  [domainname]
  domainname = example.com

This file was written by Damien Dart, <damiendart@pobox.com>. This is
free and unencumbered software released into the public domain. For more
information, please refer to the accompanying "UNLICENCE" file.
"""


import nfsnapi
import os
import unittest

try:
  from configparser import ConfigParser
  from unittest import mock
  basestring = str
except ImportError:
  from ConfigParser import ConfigParser
  import mock


class NFSNAPITests(unittest.TestCase):
  # The "fake" salt value are based on the examples used on
  # NearlyFreeSpeech.NET Members' Wiki. For more information, see
  # <https://members.nearlyfreespeech.net/wiki/API/Introduction>.
  FAKE_SALT = iter("dkwo28Sile4jdXkw")

  def setUp(self):
    config = ConfigParser()
    config.read(["nfsnapi-tests.cfg",
        os.path.expanduser("~/.nfsnapi-tests.cfg"),
        os.path.expanduser("~/nfsnapi-tests.cfg")])
    self.API_key = config.get("credentials", "apikey")
    self.account_number = config.get("credentials", "accountnumber")
    self.domain_name = config.get("domainname", "domainname")
    self.username = config.get("credentials", "username")

  @mock.patch("random.choice", lambda x: next(NFSNAPITests.FAKE_SALT))
  @mock.patch("time.time", return_value = 1012121212)
  def testAuthHeader(self, mock):
    # The expected values are based on the examples used on
    # NearlyFreeSpeech.NET Members' Wiki. For more information, see
    # <https://members.nearlyfreespeech.net/wiki/API/Introduction>.
    self.assertEqual(nfsnapi.auth_header("testuser", "p3kxmRKf9dk3l6ls",
        "/site/example/getInfo"), {"X-NFSN-Authentication" :
        "testuser;1012121212;dkwo28Sile4jdXkw;0fa8932e122d56e2f6d1550f9aab39c4aef8bfc4"})

  def testGETRequest(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "/account/%s/balance" % self.account_number), basestring)

  def testPOSTRequestWithBody(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "/dns/%s/listRRs" % self.domain_name, "type=A"), basestring)

  def testPOSTRequestWithoutBody(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "/dns/%s/listRRs" % self.domain_name, ""), basestring)

  def testRequestPathWithoutLeadingForwardSlash(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "dns/%s/listRRs" % self.domain_name, ""), basestring)

  def testBadInput(self):
    self.assertRaises(nfsnapi.NFSNAPIRequestError, nfsnapi.run_request,
      "DERP", "DERP", "/DERP", "DERP"),


if __name__ == "__main__":
  unittest.main()
