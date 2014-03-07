# -*- coding: utf-8 -*-

from flask import Flask

from config import MEMCACHED, DOUBANDB

from douban.mc import mc_from_config
from douban.beansdb import beansdb_from_config

mc = mc_from_config(MEMCACHED)
db = beansdb_from_config(DOUBANDB, mc=mc)

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
