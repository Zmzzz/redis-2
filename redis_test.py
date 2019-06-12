from api.connect_redis.redis_pool import pool
import redis
conn=redis.Redis(connection_pool=pool)
# conn.flushall()
# conn.hset('1',1,2)
print(conn.keys())
# import  datetime
# print(datetime.date.today())

import json
a={'1':3,'b':{}}
b={'2':3}
a['b']=b
print(a)