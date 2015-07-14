__author__ = 'Steve'

try:
    import MySQLdb as mdb
except ImportError:
    import pymysql as mdb
import os
import re

DEVELOPERS_TABLE = "developers"
BUYERS_TABLE = "buyers"
PRODUCTS_TABLE = "products"
ORDERS_TABLE = "orders"


class User(object):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Buyer(User):
    def __init__(self, username, password, email):
        super(self.__class__, self).__init__(username, password, email)


class Developer(User):
    def __init__(self, username, password, email):
        super(self.__class__, self).__init__(username, password, email)


def conn():
    if 'SERVER_SOFTWARE' in os.environ:
        # for SAE
        from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

        con1 = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, port=int(MYSQL_PORT))
    else:
        # for local
        from local import *

        print "connecting local mysql"

        con1 = mdb.connect(host=LOCAL_HOST, user=LOCAL_USERNAME, passwd=LOCAL_PASSWD, db=LOCAL_DB_NAME, port=LOCAL_PORT)
    return con1


def developers_authentication(con, username, password):
    cursor = con.cursor()
    es_username = re.escape(username)
    sql = "select uid,username from {0} where username='{1}' and password='{2}' ".format(DEVELOPERS_TABLE,
                                                                                         es_username,
                                                                                         password)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def buyers_authentication(con, username, password):
    cursor = con.cursor()
    es_username = re.escape(username)
    sql = "select uid,username from {0} where username='{1}' and password='{2}' ".format(BUYERS_TABLE,
                                                                                         es_username,
                                                                                         password)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def add_buyer(con, buyer):
    cursor = con.cursor()
    sql = "insert into {0} (username,password,email) values('{1}','{2}','{3}')".format(BUYERS_TABLE, buyer.username,
                                                                                       buyer.password, buyer.email)
    cursor.execute(sql)
    con.commit()


def add_developer(con, dev):
    cursor = con.cursor()
    sql = "insert into {0} (username,password,email) values('{1}','{2}','{3}')".format(DEVELOPERS_TABLE, dev.username,
                                                                                       dev.password, dev.email)
    cursor.execute(sql)
    con.commit()


def is_buyer_email_exist(con, email):
    cursor = con.cursor()
    sql = "select * from {0} where email='{1}'".format(BUYERS_TABLE, email)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        return True


def is_dev_email_exist(con, email):
    cursor = con.cursor()
    sql = "select * from {0} where email='{1}'".format(DEVELOPERS_TABLE, email)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        return True


def is_email_exist(con, email, type):
    if type == 'dev':
        return is_dev_email_exist(con, email)
    elif type == 'buyer':
        return is_buyer_email_exist(con, email)
    return False


if __name__ == "__main__":
    con = conn()
    # cursor = con.cursor()
    # sql = "select * from {0}".format(ORDERS_TABLE)
    # cursor.execute(sql)
    # r = cursor.fetchall()
    # r = buyers_authentication(con, "lily", "123")
    # print r
    u = Developer("ha", "123", "sadsaa@dasda.com")