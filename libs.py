from douban.beansdb import beansdb_from_config
from douban.sqlstore import store_from_config
from config import DOUBANDB, MYSQL_STORE

beansdb = beansdb_from_config(DOUBANDB)
sqlstore = store_from_config(MYSQL_STORE)
