DOUBANDB = {'servers':{
                '127.0.0.1:23909':range(16),
                '127.0.0.1:23910':range(16),
            },
            'proxies':['127.0.0.1:9804']
            }
DOUBANFS = {'servers':{
                '127.0.0.1:23909':range(16),
                '127.0.0.1:23910':range(16),
            },
            'proxies':['127.0.0.1:9804']
            }
DOUBANDB_SERVERS = DOUBANDB.get('servers')
DOUBANDB_PROXY = DOUBANDB.get('proxies')
DOUBANFS_SERVERS = DOUBANFS.get('servers')
DOUBANFS_PROXY = DOUBANFS.get('proxies')

MEMCACHED = {
    'servers': ["127.0.0.1:11311", ],
    'new_servers': [],
    'backup_servers': [],
    'disabled': False,
    'local_cache': True,
    'log_every_actions': False,
    'slave_servers': [],
    }
