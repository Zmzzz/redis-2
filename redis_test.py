from api.connect_redis.redis_pool import pool
import redis
conn=redis.Redis(connection_pool=pool)
# conn.flushall()
# conn.hset('1',1,2)

# import  datetime
# print(datetime.date.today())

print(conn.keys())
# # import json
# a={
#     '1':3,
#     'b':"cc"}
#
# for i,c in a.items():
#     print(i,c)
# for item in conn.scan_iter('Payment_key_1_*'):
#     print(item)
#     conn.delete(item)
# conn.delete('global_coupon_1')
# print(conn.hgetall('global_coupon_1'))a
a={
    'c':[13]
}
print(a)