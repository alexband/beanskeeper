# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import urllib
from . import rest

class BaseSession(object):

    def __init__(self, root='mybucket', rest_client=rest.RESTClient):
        self.root = root
        self.rest_client = rest_client

    def build_path(self, target, params=None):
        if sys.version_info < (3,) and isinstance(target, unicode):
            target = target.encode("utf8")

        target_path = urllib.quote(target)

        params = params or {}
        params = params.copy()

        if params:
            return (
                "%s?%s" % (
                    target_path,
                    urllib.urlencode(params))
            )

        return "%s" % target_path

    def build_url(self, host, target, params=None):
        return "http://%s%s" % (host, self.build_path(target, params))
