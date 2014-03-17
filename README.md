#### Quick Start

prepare

install beansdb from https://github.com/alexband/beansdb

install beanseye from https://github.com/douban/beanseye

install patched libmemcached

http://douban-code.github.io/pages/python-libmemcached.html

```
1. virtualenv venv
2. . venv/bin/activate
3. pip install cython

# due to http://stackoverflow.com/questions/21198881/error-when-trying-to-install-django-cms-in-virtualenv-w-mysql-on-mac-osx
4. pip install -e 'git+http://github.com/qingfeng/MySQLdb1.git@b203124b73b0018fe2da399aa363ce031392c3d4#egg=MySQL-python'

5. pip install -r requirements.txt
6. cd fnv1a ```python setup.py install```
```

BELOW ALL PORTS USED SHOULD SET IN `config.py`
start beansdb for example

```
beansdb -d -p 23909 -H /data/home/huanghuang/dbstore1 -T 1 -t 2 -v
beansdb -d -p 23910 -H /data/home/huanghuang/dbstore2 -T 1 -t 2 -v
beansdb -d -p 23911 -H /data/home/huanghuang/dbstore3 -T 1 -t 2 -v
```
install memcached, libmemcached

see http://douban-code.github.io/pages/python-libmemcached.html

start memcached

```
/usr/bin/memcached -m 64 -p 11211 -u memcache -l 127.0.0.1
```

clone beanseye & make

start beanseye as monitor & proxy

Note: beanseye is written in go, so need to setup
      go environment at first

cd to /path/to/beanseye

config conf/example.ini
set beansdb servers as you started

```./bin/proxy xxxx.ini```
setup database

```mysql -uroot```

```create database beanskeeper```

```mysql> source /path/to/beanskeeper/database/schema.sql```

set config 

cp config.py.tmpl as config.py 
change settings according

start app

```gunicorn -w 2 -b 0.0.0.0:5000 app:app```


===========================

see `example.py` for put files.
also you can ```curl "http://localhost:6000/files_put/mybucket/somefile.ext" -F file="@somefile.ext"```

beanseye should run on port 7908
http server runs on 6000

shoud see file content http://0.0.0.0:6000/files_get/mybucket/README.md
can download at http://0.0.0.0:6000/download/mybucket/README.md

============================
TODO

now only implement http PUT/GET

and using fnv1a hash as beansdb store's key also store in mysql (this will be a concern)
