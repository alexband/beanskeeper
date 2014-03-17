DOUBANDB = {'servers':{
                '127.0.0.1:23909':range(16),
                '127.0.0.1:23910':range(16),
                '127.0.0.1:23911':range(16),
            },
            'proxies':['127.0.0.1:7905']
            }
DOUBANFS = {'servers':{
                '127.0.0.1:23909':range(16),
                '127.0.0.1:23910':range(16),
                '127.0.0.1:23911':range(16),
            },
            'proxies':['127.0.0.1:7905']
            }

DOUBANDB_SERVERS = DOUBANDB.get('servers')
DOUBANDB_PROXY = DOUBANDB.get('proxies')
DOUBANFS_SERVERS = DOUBANFS.get('servers')
DOUBANFS_PROXY = DOUBANFS.get('proxies')

MEMCACHED = {
    'servers': ["127.0.0.1:11211", ],
    'new_servers': [],
    'backup_servers': [],
    'disabled': False,
    'local_cache': True,
    'log_every_actions': False,
    'slave_servers': [],
    }

MYSQL_STORE = {
    "farms": {
        "beanskeeper_farm": {
            "master": "localhost:3306:beanskeeper:root:",
            "tables": ["*"],
            }
        }
}

HOST = '0.0.0.0:6000'

try:
    from local_config import *
except ImportError, e:
    if e.args[0].startswith('No module named local_config'):
        pass
    else:
        # the ImportError is raised inside local_config
        raise
