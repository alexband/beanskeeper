# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64
import re
import os
import sys
import urllib

from StringIO import StringIO
from .rest import RESTClient

try:
    import json
except ImportError:
    import simplejson as json

class BeanskeeperClient(object):

    def __init__(self, rest_client=None):
        if rest_client is None: rest_client = RESTClient
        self.rest_client = rest_client

    def get_chunked_uploader(self, file_obj, length):
         pass

    def upload_chunk(self, file_obj, length, offset=0, upload_id=None):
         pass

    def put_file(self, full_path, file_obj, overwrite=False):
         pass

    def get_file(self, from_path):
         pass
