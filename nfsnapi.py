import hashlib
import json
import random
import string
import time
import urllib2


def auth_header(username, API_key, request_path, request_body = None):
  """Return a NearlyFreeSpeeech.NET authentication HTTP header field.

  Returns a dictionary containing an authentication HTTP header field
  required for NearlyFreeSpeech.NET API requests. For more infomation,
  see <https://members.nearlyfreespeech.net/wiki/API/Introduction>.

  - "username" should be a string containing the member login name of
    the user making the request.
  - "API_key" should be a string containing the API key assosiated with
    the member login name; an API key can be obtained by submitting a
    secure support request to NearlyFreeSpeeech.NET.
  - "request_path" should be a string containing the path portion of the
    requested URL. For example, if the requested URL is
    <https://api.nearlyfreespeech.net/site/example/addAlias>,
    "request_path" would be "/site/example/addAlias".
  - "request_body" may be a string containing the HTTP request body, or
    "None" if no such data is required. The data should be in the
    standard "application/x-www-form-urlencoded" format.
  """

  salt = "".join(random.choice(string.ascii_letters) for i in range(16))
  timestamp = str(int(time.time()))
  return { "X-NFSN-Authentication" : ";".join([username, timestamp, salt,
        hashlib.sha1(";".join([username, timestamp, salt, API_key,
        request_path, hashlib.sha1(request_body).hexdigest()])).hexdigest()])}


def run_request(username, API_key, request_path, request_body = None):
  """Run a NearlyFreeSpeech.NET API request, return a string response.

  NOTE: As this method uses the "urllib2.urlopen" function to run
  requests, the API server's certificate is not verified.

  The NearlyFreeSpeech.net API documentation is unclear on whether every
  successful API call returns a valid JSON-encoded associative array,
  hence why any response is returned as a string. This method raises
  "NFSNAPIRequestError" on errors.

  - "username" should be a string containing the member login name of
    the user making the request.
  - "API_key" should be a string containing the API key assosiated with
    the member login name; an API key can be obtained by submitting a
    secure support request to NearlyFreeSpeeech.NET.
  - "request_path" should be a string containing the path portion of the
    requested URL. For example, if the requested URL is
    <https://api.nearlyfreespeech.net/site/example/addAlias>,
    "request_path" would be "/site/example/addAlias".
  - "request_body" may be a string containing the HTTP request body, or
    "None" if no such data is required. The data should be in the
    standard "application/x-www-form-urlencoded" format.
  """

  try:
    return urllib2.urlopen(urllib2.Request(
        "https://api.nearlyfreespeech.net%s" % request_path, request_body,
        auth_header(username, API_key, request_path, request_body))).read()
  except httplib.HTTPException as e:
    raise NFSNAPIRequestError(str(e))
  except urllib2.HTTPError as e:
    try:
      error = json.loads(e.read())
      raise NFSNAPIRequestError("\n".join(error["error"], error["debug"]))
    except ValueError:
      raise NFSNAPIRequestError(str(e.reason))
  except urllib2.URLError as e:
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
