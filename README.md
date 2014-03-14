#### Quick Start

```
1. virtualenv venv
2. . venv/bin/activate
3. pip install cython
4. pip install -r requirements.txt
```

BELOW ALL PORTS USED SHOULD SET IN `config.py`
start beansdb for example

```
beansdb -d -p 23909 -H /data/home/huanghuang/dbstore1 -T 1 -t 2 -v
beansdb -d -p 23910 -H /data/home/huanghuang/dbstore2 -T 1 -t 2 -v
beansdb -d -p 23911 -H /data/home/huanghuang/dbstore3 -T 1 -t 2 -v
```

start memcached

```
/usr/bin/memcached -m 64 -p 11211 -u memcache -l 127.0.0.1
```

clone beanseye & make

start beanseye as monitor & proxy

cd to /path/to/beanseye

config conf/example.ini
set beansdb servers as you started

```./bin/proxy xxxx.ini```


start app

```gunicorn -w 2 -b 0.0.0.0:5000 app:app```
