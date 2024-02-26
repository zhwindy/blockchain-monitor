#encoding=utf-8
import os
from rediscluster import RedisCluster

HOST = [{'host': '192.168.0.147', 'port': 6379}, {'host': '192.168.0.32', 'port': 6379}, {'host': '192.168.0.246', 'port': 6379}]
PASSWD = os.getenv('NFT_REDIS_PASSWD')


def get_conn(database=None):
    conn = RedisCluster(startup_nodes=HOST, password=PASSWD)
    return conn
