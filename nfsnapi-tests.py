#!/usr/bin/env python


import ConfigParser
import nfsnapi
import os
import unittest


class NFSNAPITests(unittest.TestCase):
  def setUp(self):
    config = ConfigParser.ConfigParser()
    config.read(["nfsnapi-tests.cfg",
        os.path.expanduser("~/.nfsnapi-tests.cfg")])
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
