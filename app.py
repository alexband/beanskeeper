# -*- coding: utf-8 -*-

from flask import Flask, abort
from fnv1a import get_hash

from libs import beansdb as db, sqlstore as store
from model import BeansFile


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "hello world"

@app.route('/files_put/<bucket>/<path>', methods=["PUT", "POST"])
def files_put(bucket, path):
    filename = bucket + path
    key = get_hash(filename)
    db.set(str(key), 'somewhatkey')
    return "bucket:%s, path:%s" % (bucket, path)

@app.route('/files_get/<bucket>/<path>', methods=["GET"])
def files_get(bucket, path):
    filename = bucket + path
    key = get_hash(filename)
    content = db.get(str(key))
    if not content:
        return abort(404)

    return "%s" % content

if __name__ == "__main__":
    app.run(host="0.0.0.0")
