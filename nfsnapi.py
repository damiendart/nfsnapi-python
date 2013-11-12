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
    raise NFSNAPIRequestError(str(e), request_path)
  except urllib2.HTTPError as e:
    try:
      error = json.loads(e.read())
      raise NFSNAPIRequestError(error["error"], request_path, error["debug"])
    except ValueError:
      raise NFSNAPIRequestError(str(e.reason), request_path)
  except urllib2.URLError as e:
    raise NFSNAPIRequestError(str(e.reason), request_path)


class NFSNAPIRequestError(Exception):
  """Raised when an NearlyFreeSpeech.NET API request fails.

  Every instance will have following attributes:

  - "reason", a string with the reason for the error,
  - "request", a string containing the requested URL, and
  - "debug", a string with additional information regarding the error,
    or "None" if no such information is available.
  """

  def __init__(self, reason, request_path, debug = None):
    Exception.__init__(self, error_message)
    self.debug, self.reason, self.request = debug, reason, request_path
