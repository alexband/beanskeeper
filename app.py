# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, request, abort
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
    # curl "http://localhost:5000/files_put/mybucket/test.py" -F
    # file="@test.py"
    upload_file = request.files.get('file')
    if upload_file:
        BeansFile.add(filename=upload_file.filename,
                      mimetype=upload_file.mimetype,
                      filehash=str(key),
                      uploadTime=datetime.now())
        # to get tempfile path
        db.set(str(key), upload_file.read())
    return "bucket:%s, path:%s" % (bucket, path)


@app.route('/files_get/<bucket>/<path>', methods=["GET"])
def files_get(bucket, path):
    filename = bucket + path
    key = get_hash(filename)
    beansfile = BeansFile.get_by_filehash(str(key))
    if beansfile:
        content = beansfile.content()
        if content:
            return "%s" % content
    return abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    # or run with gunicorn -w 2 -b 0.0.0.0:5000 app:app
