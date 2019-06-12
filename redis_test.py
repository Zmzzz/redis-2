from api.connect_redis.redis_pool import pool
import redis
conn=redis.Redis(connection_pool=pool)
# conn.flushall()
# conn.hset('1',1,2)
print(conn.hgetall('LuffyCourse_1_2'))

