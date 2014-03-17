# -*- coding: utf-8 -*-
import os

from client.client import BeanskeeperClient

from client.client import BeanskeeperClient

c = BeanskeeperClient()
filename = os.path.dirname(os.path.realpath(__file__)) + '/README.md'

f = open(filename, 'r')
c.put_file('/README.md', f.read())

