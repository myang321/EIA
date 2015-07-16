__author__ = 'Steve'

try:
    import MySQLdb as mdb
except ImportError:
    import pymysql as mdb
import os
import re
from random import randint

DEVELOPERS_TABLE = "developers"
BUYERS_TABLE = "buyers"
PRODUCTS_TABLE = "products"
ORDERS_TABLE = "orders"
IMG_TABLE = "img"

CATEGORY_FUNCTION = "category_function"
CATEGORY_UI_STYLE = "category_ui_style"
UPLOAD_FOLDER = 'static/upload/'


def get_random_number_str():
    return str(randint(1111, 99999999))


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


class Product(object):
    def __init__(self, title='', price='', description='', c_func='', c_ui='', dev_uid='', img_list=None):
        self.title = title
        self.price = price
        self.description = description
        self.c_func = c_func
        self.c_ui = c_ui
        self.dev_uid = dev_uid
        self.img_list = img_list
        if self.img_list:
            if 'SERVER_SOFTWARE' not in os.environ:
                self.img_list = ['/' + UPLOAD_FOLDER + str for str in self.img_list]


def conn():
    if 'SERVER_SOFTWARE' in os.environ:
        # for SAE
        from sae.const import (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

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
    sql = "select * from developers where email='{0}'".format(email)
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


def get_category_function_id(con, title):
    cursor = con.cursor()
    sql = "select cid from {0} where title='{1}'".format(CATEGORY_FUNCTION, title)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


def get_category_function_title(con, id):
    cursor = con.cursor()
    sql = "select title from {0} where cid={1}".format(CATEGORY_FUNCTION, id)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


def get_category_ui_style_id(con, title):
    cursor = con.cursor()
    sql = "select cid from {0} where title='{1}'".format(CATEGORY_UI_STYLE, title)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


def get_category_ui_style_title(con, id):
    cursor = con.cursor()
    sql = "select title from {0} where cid={1}".format(CATEGORY_UI_STYLE, id)
    print sql
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


def search_by_category(con, c_func, c_ui):
    if c_func == 'all' and c_ui == 'all':
        sql = "select * from {0}".format(PRODUCTS_TABLE)
    elif c_ui == 'all':
        sql = "select * from {0} where c_function={1}".format(PRODUCTS_TABLE, get_category_function_id(con, c_func))
    elif c_func == 'all':
        sql = "select * from {0} where c_ui_style={1}".format(PRODUCTS_TABLE, get_category_ui_style_id(con, c_ui))
    else:
        sql = "select * from {0} where c_function={1} and c_ui_style={2}".format(PRODUCTS_TABLE,
                                                                                 get_category_function_id(con, c_func),
                                                                                 get_category_ui_style_id(con, c_ui))
    print sql
    result = execute_select_all(con, sql)
    list1 = []
    for row in result:
        product = relation_to_object_mapping_product(con, row)
        list1.append(product)
    return list1


def relation_to_object_mapping_product(con, row):
    pid = row[0]
    product = Product(title=row[1], price=row[4], description=row[3], c_func=get_category_function_title(con, row[6]),
                      c_ui=get_category_ui_style_title(con, row[7]), dev_uid=row[2], img_list=get_product_img(con, pid))
    return product


def get_category_function_list(con):
    cursor = con.cursor()
    sql = "SELECT title from {0}".format(CATEGORY_FUNCTION)
    cursor.execute(sql)
    result = cursor.fetchall()
    # convert to list
    list1 = [row[0] for row in result]
    return list1


def get_category_ui_style_list(con):
    cursor = con.cursor()
    sql = "SELECT title from {0}".format(CATEGORY_UI_STYLE)
    cursor.execute(sql)
    result = cursor.fetchall()
    # convert to list
    list1 = [row[0] for row in result]
    return list1


def get_product_detail(con, title):
    sql = "SELECT * from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
    result = execute_select_one(con, sql)
    product = relation_to_object_mapping_product(con, result)
    print product.img_list
    return product


def get_product_id(con, title):
    cursor = con.cursor()
    sql = "SELECT pid from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


# def get_buyer_id(con, name):
# cursor = con.cursor()
# sql = "SELECT pid from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
# cursor.execute(sql)
# result = cursor.fetchone()
# return result[0]

def create_order(con, title, buyer_id):
    pid = get_product_id(con, title)
    sql = "insert into {0} (pid,buyer_uid) values({1},{2})".format(ORDERS_TABLE, pid, buyer_id)
    execute_non_query(con, sql)


def has_bought(con, title, buyer_id):
    cursor = con.cursor()
    pid = get_product_id(con, title)
    sql = "select * from {0} where pid={1} and buyer_uid={2}".format(ORDERS_TABLE, pid, buyer_id)
    cursor.execute(sql)
    result = cursor.fetchone()
    print result
    if result != None:
        return True
    else:
        return False


def get_buyer_orders(con, bid):
    sql = "select p.*,o.date from {0}  as p, {1} as o where o.buyer_uid={2} and p.pid=o.pid".format(PRODUCTS_TABLE,
                                                                                                    ORDERS_TABLE, bid)
    result = execute_select_all(con, sql)
    list1 = []
    for row in result:
        product = relation_to_object_mapping_product(con, row)
        list1.append(product)
    return list1


def get_developers_products(con, dev_id):
    sql = "select * from {0} where dev_uid={1}".format(PRODUCTS_TABLE, dev_id)
    result = execute_select_all(con, sql)
    list1 = []
    for row in result:
        product = relation_to_object_mapping_product(con, row)
        list1.append(product)
    return list1


def get_developer_orders(con, dev_id):
    sql = "select * from {0} as p , {1} as o where p.dev_uid={2} and o.pid=p.pid".format(PRODUCTS_TABLE,
                                                                                         ORDERS_TABLE, dev_id)
    result = execute_select_all(con, sql)
    list1 = []
    for row in result:
        product = relation_to_object_mapping_product(con, row)
        list1.append(product)
    return list1


def save_product(con, p):
    sql = "insert into {0} (title,dev_uid,description,price,c_function,c_ui_style) values('{1}',{2},'{3}',{4},{5},{6})".format(
        PRODUCTS_TABLE, p.title, p.dev_uid, p.description, p.price, get_category_function_id(con, p.c_func),
        get_category_ui_style_id(con, p.c_ui))
    execute_non_query(con, sql)
    pid = get_product_id(con, p.title)
    return pid


def update_product(con, p, old_title):
    sql = "update {0} set title='{1}' , price={2}, description='{3}' , c_function={4}, c_ui_style={5} where title='{6}'".format(
        PRODUCTS_TABLE, p.title, p.price, p.description, get_category_function_id(con, p.c_func),
        get_category_ui_style_id(con, p.c_ui), old_title)
    execute_non_query(con, sql)
    pid = get_product_id(con, p.title)
    return pid


def save_img_url(con, url, pid, is_front):
    sql = "insert into {0} (url,pid,front) values('{1}',{2},{3})".format(IMG_TABLE, url, pid, is_front)
    execute_non_query(con, sql)


def execute_select_one(con, sql):
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def execute_select_all(con, sql):
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def execute_non_query(con, sql):
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()


def save_image(con, file1, pid):
    # filename = str(pid) + '_' + get_random_number_str() + '_' + file1.filename
    ext = file1.filename.split('.')[-1]
    filename = str(pid) + get_random_number_str() + '.' + ext
    print "save image file1 name", file1.filename
    if 'SERVER_SOFTWARE' in os.environ:
        from sae.storage import Bucket

        bucket = Bucket('domain1')
        bucket.put_object(filename, file1)
        url = bucket.generate_url(filename)
    else:
        url = filename
        file_full_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.environ['USER'] == 'lily':
            file_full_path = "/Users/Lily/PycharmProjects/EIA/static/upload/" + filename
        print file_full_path
        file1.save(file_full_path)
    save_img_url(con, url, pid, 1)


def get_product_img(con, pid):
    sql = "select url from {0} where pid={1} order by front desc".format(IMG_TABLE, pid)
    result = execute_select_all(con, sql)
    list1 = [row[0] for row in result]
    return list1


def delete_product(con, p_title):
    sql = "delete from {0} where title='{1}'".format(PRODUCTS_TABLE, p_title)
    execute_non_query(con, sql)


if __name__ == "__main__":
    con = conn()
    # cursor = con.cursor()
    # sql = "select * from {0}".format(ORDERS_TABLE)
    # cursor.execute(sql)
    # r = cursor.fetchall()
    # r = buyers_authentication(con, "lily", "123")
    # r=get_category_function_id(con,"travel")
    # r = get_category_ui_style_id(con, "plain")
    # r = search_by_category(con, "travel", "plain")
    # r = get_category_function_list(con)
    # r = get_category_ui_style_list(con)
    # r = get_category_ui_style_title(con, 2)
    # r = get_product_detail(con, 'airbnb')
    r = get_buyer_orders(con, 1)
    print r
    # u = Developer("ha", "123", "sadsaa@dasda.com")