# -*- coding: utf-8 -*-
import StringIO
from datetime import datetime
from MySQLdb import IntegrityError
from flask import (Flask, request, abort,
                   send_file)
from fnv1a import get_hash

from libs import beansdb as db
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
    else:
        data = request.data
        if data:
            try:
                BeansFile.add(filename=path,
                          mimetype="application/octet-stream",
                          filehash=str(key),
                          uploadTime=datetime.now())
            except IntegrityError:
                oldfile = BeansFile.get_by_filehash(str(key))
                oldfile.uploadTime=datetime.now()
                oldfile.save()
            db.set(str(key), data)
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

@app.route('/download/<bucket>/<path>', methods=["GET"])
def download(bucket, path):
    filename = bucket + path
    key = get_hash(filename)
    beansfile = BeansFile.get_by_filehash(str(key))

    if not beansfile:
        return abort(404)

    return send_file(StringIO.StringIO(beansfile.content()),
                     mimetype="application/octet-stream",
                     cache_timeout=2592000,
                     as_attachment=True,
                     attachment_filename=beansfile.filename.encode("UTF-8"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    # or run with gunicorn -w 2 -b 0.0.0.0:5000 app:app
