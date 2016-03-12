"""Stuff to make working with the NearlyFreeSpeech.NET API easier.

  >>> import nfsnapi
  >>> # Replace USERNAME, API_KEY, and so on with actual values.
  >>> nfsnapi.run_request("USERNAME", "API_KEY",
  ... "/account/ACCOUNT_NUMBER/balance")
  '10.56'
  >>> nfsnapi.run_request("USERNAME", "API_KEY",
  ... "/dns/DOMAIN/listRRs", "type=A")
  (A bunch of JSON not shown.)
  >>> # And so on...

This file was written by Damien Dart, <damiendart@pobox.com>. This is
free and unencumbered software released into the public domain. For more
information, please refer to the accompanying "UNLICENCE" file.
"""

__author__ = "Damien Dart, <damiendart@pobox.com>"
__license__ = "Unlicense"
__title__ = "nfsnapi"
__version__ = "0.2.0"


import json
import random
import string
import time

from hashlib import sha1

try:
  from http.client import HTTPException
  from urllib.request import urlopen, Request
  from urllib.error import HTTPError, URLError
  basestring = str
except ImportError:
  from httplib import HTTPException
  from urllib2 import urlopen, Request, HTTPError, URLError


def auth_header(username, API_key, request_path, request_body = b""):
  """Return a NearlyFreeSpeeech.NET authentication HTTP header field.

  Returns a dictionary containing an authentication HTTP header field
  required for NearlyFreeSpeech.NET API requests. For more information,
  see <https://members.nearlyfreespeech.net/wiki/API/Introduction>.

  - "username" should be a string containing the member login name of
    the user making the request.
  - "API_key" should be a string containing the API key associated with
    the member login name; an API key can be obtained by submitting a
    secure support request to NearlyFreeSpeeech.NET.
  - "request_path" should be a string containing the path portion of the
    requested URL. For example, if the requested URL is
    <https://api.nearlyfreespeech.net/site/example/addAlias>,
    "request_path" would be "/site/example/addAlias". The first
    forward-slash is optional.
  - "request_body" may be a bytestring containing the HTTP request
    message body for HTTP POST requests, or an empty bytestring for GET
    requests or if no such data is required. The data should be in the
    standard "application/x-www-form-urlencoded" format.
  """

  if (request_path[0] != "/"):
    request_path = "/%s" % request_path
  salt = "".join(random.choice(string.ascii_letters) for i in range(16))
  timestamp = str(int(time.time()))
  return { "X-NFSN-Authentication" : ";".join([username, timestamp, salt,
      sha1(str(";".join([username, timestamp, salt, API_key, request_path,
      sha1(request_body).hexdigest()])).encode("utf-8")).hexdigest()]) }


def run_request(username, API_key, request_path, request_body = None):
  """Run a NearlyFreeSpeech.NET API request, return a string response.

  NOTE: This function does not verify the API server's certificate.

  The NearlyFreeSpeech.net API documentation is unclear on whether every
  successful API call returns a valid JSON-encoded associative array,
  hence why any response is returned as a string. This method raises
  "NFSNAPIRequestError" on errors.

  - "username" should be a string containing the member login name of
    the user making the request.
  - "API_key" should be a string containing the API key associated with
    the member login name; an API key can be obtained by submitting a
    secure support request to NearlyFreeSpeeech.NET.
  - "request_path" should be a string containing the path portion of the
    requested URL. For example, if the requested URL is
    <https://api.nearlyfreespeech.net/site/example/addAlias>,
    "request_path" would be "/site/example/addAlias". The first
    forward-slash is optional.
  - "request_body" may be a string containing the HTTP request message
    body for HTTP POST requests or "None" for HTTP GET requests. Pass
    an empty string for HTTP POST requests that do not require a message
    body. The data should be in the standard
    "application/x-www-form-urlencoded" format.
  """

  try:
    if (request_path[0] != "/"):
      request_path = "/%s" % request_path
    if isinstance(request_body, basestring):
      request_body = request_body.encode("utf-8")
    return urlopen(Request("https://api.nearlyfreespeech.net" + request_path,
        request_body, dict(auth_header(username, API_key, request_path,
        request_body or b""), **{"User-Agent": "nfsnapi/" + __version__ +
        " +http://www.robotinaponcho.net/git/nfsnapi-python.git/"}))).read().decode()
  except HTTPException as e:
    raise NFSNAPIRequestError(str(e))
  except HTTPError as e:
    try:
      error = json.loads(e.read().decode())
      raise NFSNAPIRequestError("\n".join([error["error"], error["debug"]]))
    except (KeyError, ValueError):
      raise NFSNAPIRequestError(str(e.reason))
  except URLError as e:
    raise NFSNAPIRequestError(str(e.reason))


class NFSNAPIRequestError(Exception):
  """Raised when an NearlyFreeSpeech.NET API request fails.

  Every instance will have a "reason" attribute, a string with the
  reason for the error. If the offending request resulted in a 4XX or
  5XX HTTP response, the attribute will contain the "human-readable" and
  debug error messages returned by the NearlyFreeSpeech.NET API,
  separated by a new-line (for more information, see
  <https://members.nearlyfreespeech.net/wiki/API/Introduction>).
  """

  def __init__(self, reason):
    Exception.__init__(self, reason)
    self.reason = reason
