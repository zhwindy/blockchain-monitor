# encoding=utf-8
import pymysql
import os

host = os.getenv('NFT_MYSQL_HOST')
user = os.getenv('NFT_MYSQL_USER')
passwd = os.getenv('NFT_MYSQL_PASSWD')

conn = pymysql.connect(host=host, user=user, passwd=passwd, db='', charset='utf8')
