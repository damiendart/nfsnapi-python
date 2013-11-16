#!/usr/bin/env python

"""Tests for the "nfsnapi" module.

These tests do not modify any of your settings. To run these tests you
must have an account with NearlyFreeSpeech.NET, along with:

  - an API key for your account provided by NearlyFreeSpeech.NET and
  - a domain name whose DNS is managed by NearlyFreeSpeech.NET.

Credentials and other required information are read from a
"nfsnapi-tests.cfg" file located either in the current directory or the
home directory of the user running the tests. This file must contain the
following information (replace dummy values with your own details):

  [credentials]
  accountnumber = A1B2-C3D4E5F6
  apikey = abcdefgh12345678
  username = testuser
  [domainname]
  domainname = example.com
"""


import ConfigParser
import nfsnapi
import os
import unittest


class NFSNAPITests(unittest.TestCase):
  def setUp(self):
    config = ConfigParser.ConfigParser()
    config.read(["nfsnapi-tests.cfg",
        os.path.expanduser("~/.nfsnapi-tests.cfg"),
        os.path.expanduser("~/nfsnapi-tests.cfg")])
    self.API_key = config.get("credentials", "apikey")
    self.account_number = config.get("credentials", "accountnumber")
    self.domain_name = config.get("domainname", "domainname")
    self.username = config.get("credentials", "username")

  def testGETRequest(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "/account/%s/balance" % self.account_number), str)

  def testPOSTRequestWithBody(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "/dns/%s/listRRs" % self.domain_name, "type=A"), str)

  def testPOSTRequestWithoutBody(self):
    self.assertIsInstance(nfsnapi.run_request(self.username, self.API_key,
        "/dns/%s/listRRs" % self.domain_name, ""), str)

  def testBadInput(self):
    self.assertRaises(nfsnapi.NFSNAPIRequestError, nfsnapi.run_request,
      "DERP", "DERP", "DERP", "DERP"),


if __name__ == "__main__":
  unittest.main()
