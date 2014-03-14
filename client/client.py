# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64
import re
import os
import sys
import urllib

from StringIO import StringIO
from .session import BaseSession
from .rest import RESTClient

try:
    import json
except ImportError:
    import simplejson as json


class BeanskeeperClient(object):

    def __init__(self, root='mybucket', rest_client=None):
        if rest_client is None:
            rest_client = RESTClient
        self.rest_client = rest_client
        self.session = BaseSession(root=root,
                                   rest_client=rest_client)

    def request(self, target, params=None,
                method='POST', content_server=False):
        assert method in [
            'GET', 'POST', 'PUT'], "Only 'GET', 'POST', and 'PUT' are allowed."
        if params is None:
            params = {}

        host = self.session.HOST
        url = self.session.build_url(host, target, params)
        return url

    def get_chunked_uploader(self, file_obj, length):
        pass

    def upload_chunk(self, file_obj, length, offset=0, upload_id=None):
        pass

    def put_file(self, target_path, file_obj, overwrite=False):
        """
        >>> f = open('/path/to/filename.ext', 'r')
        >>> c.put_file('/filename.txt', f.read())
        """

        path = "/files_put/%s%s" % (self.session.root, target_path)
        url = self.request(path, method='PUT')
        return self.rest_client.PUT(url, file_obj, raw_response=True)

    def get_file(self, from_path):
        pass
