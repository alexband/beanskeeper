from douban.beansdb import beansdb_from_config
from douban.sqlstore import store_from_config
from douban.mc import mc_from_config
from ORZ import setup
from config import DOUBANDB, MEMCACHED, MYSQL_STORE

mc = mc_from_config(MEMCACHED)
beansdb = beansdb_from_config(DOUBANDB)
sqlstore = store_from_config(MYSQL_STORE)
setup(sqlstore, mc)
