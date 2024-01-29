#encoding=utf-8
import os
import pymysql

HOST = os.getenv('NFT_MYSQL_HOST')
PORT = 4000
USER = os.getenv('NFT_MYSQL_USER')
PASSWD = os.getenv('NFT_MYSQL_PASSWD')


def get_conn(database=None):
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=database, charset='utf8')
    return conn
