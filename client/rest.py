# -*- coding: utf-8 -*-

"""This file is derived from Dropbox Python SDK"""

import io
import pkg_resources
import socket
import ssl
import sys
import urllib

try:
    import json
except ImportError:
    import simplejson as json

try:
    import urllib3
except ImportError:
    raise ImportError('client requires urllib3')


class RESTResponse(io.IOBase):

    def __init__(self, resp):
        # arg: A urllib3.HTTPResponse object
        self.urllib3_response = resp
        self.status = resp.status
        self.version = resp.version
        self.reason = resp.reason
        self.strict = resp.strict
        self.is_closed = False

    def __del__(self):
        # Attempt to close when ref-count goes to zero.
        self.close()

    def __exit__(self, typ, value, traceback):
        # Allow this to be used in "with" blocks.
        self.close()

    # -----------------
    # Important methods
    # -----------------
    def read(self, amt=None):
        if self.is_closed:
            raise ValueError('Response already closed')
        return self.urllib3_response.read(amt)

    BLOCKSIZE = 4 * 1024 * 1024  # 4MB at a time just because

    def close(self):
        """Closes the underlying socket."""

        # Double closing is harmless
        if self.is_closed:
            return

        # Read any remaining crap off the socket before releasing the
        # connection. Buffer it just in case it's huge
        while self.read(RESTResponse.BLOCKSIZE):
            pass

        # Mark as closed and release the connection (exactly once)
        self.is_closed = True
        self.urllib3_response.release_conn()

    @property
    def closed(self):
        return self.is_closed

    # ---------------------------------
    # Backwards compat for HTTPResponse
    # ---------------------------------
    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.urllib3_response.getheaders()

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.urllib3_response.getheader(name, default)

    # Some compat functions showed up recently in urllib3
    try:
        urllib3.HTTPResponse.flush
        urllib3.HTTPResponse.fileno

        def fileno(self):
            return self.urllib3_response.fileno()

        def flush(self):
            return self.urllib3_response.flush()
    except AttributeError:
        pass


def create_connection(address):
    host, port = address
    err = None
    for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket.socket(af, socktype, proto)
            sock.connect(sa)
            return sock

        except socket.error as e:
            err = e
            if sock is not None:
                sock.close()

    if err is not None:
        raise err # pylint: disable-msg=E0702
    else:
        raise socket.error("getaddrinfo returns an empty list")


def json_loadb(data):
    if sys.version_info >= (3,):
        data = data.decode('utf8')
    return json.loads(data)


class RESTClientObject(object):

    def __init__(self, max_reusable_connections=8, mock_urlopen=None):
        self.mock_urlopen = mock_urlopen
        self.pool_manager = urllib3.PoolManager(
            num_pools=4,
            # only a handful of hosts. api.dropbox.com,
            # api-content.dropbox.com
            maxsize=max_reusable_connections,
            block=False,
            timeout=60.0,
            # long enough so datastores await doesn't get interrupted
        )

    def request(self, method, url, post_params=None,
                body=None, headers=None, raw_response=False):
        """Performs a REST request. See :meth:`RESTClient.request()` for detailed description."""

        post_params = post_params or {}
        headers = headers or {}
        headers['User-Agent'] = 'BeanskeeperClient'

        if post_params:
            if body:
                raise ValueError(
                    "body parameter cannot be used with post_params parameter")
            body = urllib.urlencode(post_params)
            headers["Content-type"] = "application/x-www-form-urlencoded"

        # Handle StringIO instances, because urllib3 doesn't.
        if hasattr(body, 'getvalue'):
            body = str(body.getvalue())
            headers["Content-Length"] = len(body)

        # Reject any headers containing newlines; the error from the server
        # isn't pretty.
        for key, value in headers.items():
            if isinstance(value, basestring) and '\n' in value:
                raise ValueError(
                    "headers should not contain newlines (%s: %s)" %
                    (key, value))

        try:
            # Grab a connection from the pool to make the request.
            # We return it to the pool when caller close() the response
            urlopen = self.mock_urlopen if self.mock_urlopen else self.pool_manager.urlopen
            r = urlopen(
                method=method,
                url=url,
                body=body,
                headers=headers,
                preload_content=False
            )
            # wrap up the urllib3 response before proceeding
            r = RESTResponse(r)
        except socket.error as e:
            raise RESTSocketError(url, e)
        except urllib3.exceptions.SSLError as e:
            raise RESTSocketError(url, "SSL certificate error: %s" % e)

        if r.status != 200:
            raise ErrorResponse(r, r.read())

        return self.process_response(r, raw_response)

    def process_response(self, r, raw_response):
        if raw_response:
            return r
        else:
            s = r.read()
            try:
                resp = json_loadb(s)
            except ValueError:
                raise ErrorResponse(r, s)
            r.close()

        return resp

    def GET(self, url, headers=None, raw_response=False):
        assert isinstance(raw_response, bool)
        return (
            self.request(
                "GET",
                url,
                headers=headers,
                raw_response=raw_response)
        )

    def POST(self, url, params=None, headers=None, raw_response=False):
        assert isinstance(raw_response, bool)
        if params is None:
            params = {}

        return self.request("POST", url,
                            post_params=params, headers=headers, raw_response=raw_response)

    def PUT(self, url, body, headers=None, raw_response=False):
        assert isinstance(raw_response, bool)
        return (
            self.request(
                "PUT",
                url,
                body=body,
                headers=headers,
                raw_response=raw_response)
        )


class RESTClient(object):

    IMPL = RESTClientObject()

    @classmethod
    def request(cls, *n, **kw):
        return cls.IMPL.request(*n, **kw)

    @classmethod
    def GET(cls, *n, **kw):
        """Perform a GET request using :meth:`RESTClient.request()`."""
        return cls.IMPL.GET(*n, **kw)

    @classmethod
    def POST(cls, *n, **kw):
        """Perform a POST request using :meth:`RESTClient.request()`."""
        return cls.IMPL.POST(*n, **kw)

    @classmethod
    def PUT(cls, *n, **kw):
        """Perform a PUT request using :meth:`RESTClient.request()`."""
        return cls.IMPL.PUT(*n, **kw)


class RESTSocketError(socket.error):

    """A light wrapper for ``socket.error`` that adds some more information."""

    def __init__(self, host, e):
        msg = "Error connecting to \"%s\": %s" % (host, str(e))
        socket.error.__init__(self, msg)


# Dummy class for docstrings, see doco.py.
class _ErrorResponse__doc__(Exception):

    _status__doc__ = "HTTP response status (an int)."
    _reason__doc__ = "HTTP response reason (a string)."
    _body__doc__ = "HTTP response body (string or JSON dict)."
    _headers__doc__ = "HTTP response headers (a list of (header, value) tuples)."
    _error_msg__doc__ = "Error message for developer (optional)."
    _user_error_msg__doc__ = "Error message for end user (optional)."


class ErrorResponse(Exception):

    def __init__(self, http_resp, body):

        self.status = http_resp.status
        self.reason = http_resp.reason
        self.body = body
        self.headers = http_resp.getheaders()
        http_resp.close()  # won't need this connection anymore

        try:
            self.body = json_loadb(self.body)
            self.error_msg = self.body.get('error')
            self.user_error_msg = self.body.get('user_error')
        except ValueError:
            self.error_msg = None
            self.user_error_msg = None

    def __str__(self):
        if self.user_error_msg and self.user_error_msg != self.error_msg:
            # one is translated and the other is English
            msg = "%r (%r)" % (self.user_error_msg, self.error_msg)
        elif self.error_msg:
            msg = repr(self.error_msg)
        elif not self.body:
            msg = repr(self.reason)
        else:
            msg = "Error parsing response body or headers: " +\
                  "Body - %.100r Headers - %r" % (self.body, self.headers)

        return "[%d] %s" % (self.status, msg)
