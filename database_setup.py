import sys

reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'Steve'

try:
    import MySQLdb as mdb
except ImportError:
    import pymysql as mdb
import os
import re
from random import randint
import smtplib
from threading import Thread

DEVELOPERS_TABLE = "developers"
BUYERS_TABLE = "buyers"
PRODUCTS_TABLE = "products"
ORDERS_TABLE = "orders"
IMG_TABLE = "img"

CATEGORY_FUNCTION_TABLE = "category_function"
CATEGORY_UI_STYLE_TABLE = "category_ui_style"
UPLOAD_FOLDER = 'static/upload/'


def get_random_number_str():
    return str(randint(1111, 99999999))


class User(object):
    def __init__(self, username, password, email, uid):
        self.username = username
        self.password = password
        self.email = email


class Category(object):
    def __init__(self, cid, title, description=None):
        self.cid = cid
        self.title = title
        self.description = description


class CategoryFunction(Category):
    def __init__(self, cid, title, description=None):
        super(self.__class__, self).__init__(cid, title, description)


class CategoryUIStyle(Category):
    def __init__(self, cid, title, description=None):
        super(self.__class__, self).__init__(cid, title, description)


class Buyer(User):
    def __init__(self, username=None, password=None, email=None, uid=None):
        super(self.__class__, self).__init__(username, password, email, uid)


class Developer(User):
    def __init__(self, username=None, password=None, email=None, uid=None):
        super(self.__class__, self).__init__(username, password, email, uid)


class Product(object):
    def __init__(self, title='', price='', description='', c_func='', c_ui='', dev_uid='', img_list=None, pid=None):
        self.title = title
        self.price = price
        self.description = re.escape(description)
        self.c_func = c_func
        self.c_ui = c_ui
        self.dev_uid = dev_uid
        self.img_list = img_list
        self.pid = pid
        if self.img_list:
            if 'SERVER_SOFTWARE' not in os.environ:
                self.img_list = ['/' + UPLOAD_FOLDER + str for str in self.img_list]
        if self.img_list == None or len(self.img_list) == 0:
            self.img_list = ['/static/img/no_image2.png']

    def get_description(self):
        print self.description
        str = self.description.decode('string_escape')
        str = str.replace('\\', '')
        print str
        return str


class SendEmailThread(Thread):
    def __init__(self, to_addrs, buyer, product_title):
        Thread.__init__(self)
        self.to_addrs = to_addrs
        self.buyer = buyer
        self.product_title = product_title

    def run(self):
        buyer = self.buyer
        product_title = self.product_title
        to_addrs = self.to_addrs
        # Credentials (if needed)
        username = 'applatform.service@gmail.com'
        password = 'eiawestart'
        from_addr = username
        subject = 'Order Notification'
        url = 'http://applatform.sinaapp.com/'
        content = "{0} has bought your product: {1}\nThis is {0}'s email: {2}\n\n{3}".format(buyer.username,
                                                                                             product_title,
                                                                                             buyer.email, url)
        message = '\From: {0}\nTo: {1}\nSubject: {2}\n\n{3}'.format(username, ", ".join([to_addrs]), subject, content)

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message)
        server.close()


def conn():
    if 'SERVER_SOFTWARE' in os.environ:
        # for SAE
        from sae.const import (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

        con1 = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, port=int(MYSQL_PORT))
    else:
        # for local
        from local import *

        print "connecting local mysql"

        con1 = mdb.connect(host=LOCAL_HOST, user=LOCAL_USERNAME, passwd=LOCAL_PASSWD, db=LOCAL_DB_NAME,
                           port=LOCAL_PORT, charset='utf8')
    return con1


def developers_authentication(con, username, password):
    es_username = re.escape(username)
    sql = "select uid,username from {0} where username='{1}' and password='{2}' ".format(DEVELOPERS_TABLE,
                                                                                         es_username,
                                                                                         password)
    result = execute_select_one(con, sql)
    return result


def buyers_authentication(con, username, password):
    es_username = re.escape(username)
    sql = "select uid,username from {0} where username='{1}' and password='{2}' ".format(BUYERS_TABLE,
                                                                                         es_username,
                                                                                         password)
    result = execute_select_one(con, sql)
    return result


def add_buyer(con, buyer):
    sql = "insert into {0} (username,password,email) values('{1}','{2}','{3}')".format(BUYERS_TABLE, buyer.username,
                                                                                       buyer.password, buyer.email)
    execute_non_query(con, sql)


def add_developer(con, dev):
    sql = "insert into {0} (username,password,email) values('{1}','{2}','{3}')".format(DEVELOPERS_TABLE, dev.username,
                                                                                       dev.password, dev.email)
    execute_non_query(con, sql)


def is_buyer_email_exist(con, email):
    sql = "select * from {0} where email='{1}'".format(BUYERS_TABLE, email)
    result = execute_select_one(con, sql)
    if result == None:
        return False
    else:
        return True


def is_dev_email_exist(con, email):
    sql = "select * from developers where email='{0}'".format(email)
    result = execute_select_one(con, sql)
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


def get_category_id(con, title, table_name):
    sql = "select cid from {0} where title='{1}'".format(table_name, title)
    result = execute_select_one(con, sql)
    return result[0]


def get_category_title(con, id, table_name):
    sql = "select title from {0} where cid={1}".format(table_name, id)
    result = execute_select_one(con, sql)
    return result[0]


def search_by_category(con, c_func, c_ui):
    if c_func == 'all' and c_ui == 'all':
        sql = "select * from {0}".format(PRODUCTS_TABLE)
    elif c_ui == 'all':
        sql = "select * from {0} where c_function={1}".format(PRODUCTS_TABLE,
                                                              get_category_id(con, c_func, CATEGORY_FUNCTION_TABLE))
    elif c_func == 'all':
        sql = "select * from {0} where c_ui_style={1}".format(PRODUCTS_TABLE,
                                                              get_category_id(con, c_ui, CATEGORY_UI_STYLE_TABLE))
    else:
        sql = "select * from {0} where c_function={1} and c_ui_style={2}".format(PRODUCTS_TABLE,
                                                                                 get_category_id(con, c_func,
                                                                                                 CATEGORY_FUNCTION_TABLE),
                                                                                 get_category_id(con, c_ui,
                                                                                                 CATEGORY_UI_STYLE_TABLE))
    result = execute_select_all(con, sql)
    list1 = []
    for row in result:
        product = relation_to_object_mapping_product(con, row)
        list1.append(product)
    return list1


def relation_to_object_mapping_product(con, row):
    pid = row[0]
    product = Product(title=row[1], price=row[4], description=row[3],
                      c_func=get_category_title(con, row[6], CATEGORY_FUNCTION_TABLE),
                      c_ui=get_category_title(con, row[7], CATEGORY_UI_STYLE_TABLE), dev_uid=row[2],
                      img_list=get_product_img(con, pid),
                      pid=pid)
    return product


def relation_to_object_mapping_developer(con, row):
    dev = Developer(uid=row[0], username=row[1], email=row[3])
    return dev


def relation_to_object_mapping_buyer(con, row):
    buyer = Buyer(uid=row[0], username=row[1], email=row[3])
    return buyer


def relation_to_object_mapping_category_function(con, row):
    c_func = CategoryFunction(cid=row[0], title=row[1], description=row[3])
    return c_func


def relation_to_object_mapping_category_ui_style(con, row):
    c_ui = CategoryUIStyle(cid=row[0], title=row[1], description=row[3])
    return c_ui


def get_category_function_list(con):
    sql = "SELECT * from {0}".format(CATEGORY_FUNCTION_TABLE)
    result = execute_select_all(con, sql)
    # convert to list
    list1 = [CategoryFunction(cid=row[0], title=row[1]) for row in result]
    return list1


def get_category_ui_style_list(con):
    sql = "SELECT * from {0}".format(CATEGORY_UI_STYLE_TABLE)
    result = execute_select_all(con, sql)
    # convert to list
    list1 = [CategoryUIStyle(cid=row[0], title=row[1]) for row in result]
    return list1


def get_product_detail(con, title):
    sql = "SELECT * from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
    result = execute_select_one(con, sql)
    product = relation_to_object_mapping_product(con, result)
    return product


def get_buyer(con, uid):
    sql = "SELECT * from {0} where uid='{1}'".format(BUYERS_TABLE, uid)
    result = execute_select_one(con, sql)
    buyer = relation_to_object_mapping_buyer(con, result)
    return buyer


def get_developer(con, uid):
    sql = "SELECT * from {0} where uid='{1}'".format(DEVELOPERS_TABLE, uid)
    result = execute_select_one(con, sql)
    buyer = relation_to_object_mapping_developer(con, result)
    return buyer


# def get_product_id(con, title):
# cursor = con.cursor()
# sql = "SELECT pid from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
# cursor.execute(sql)
# result = cursor.fetchone()
# return result[0]


# def get_buyer_id(con, name):
# cursor = con.cursor()
# sql = "SELECT pid from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
# cursor.execute(sql)
# result = cursor.fetchone()
# return result[0]

def create_order(con, title, buyer_id):
    p = get_product_detail(con, title)
    sql = "insert into {0} (pid,buyer_uid) values({1},{2})".format(ORDERS_TABLE, p.pid, buyer_id)
    execute_non_query(con, sql)
    buyer = get_buyer(con, buyer_id)
    developer = get_developer(con, p.dev_uid)
    send_mail(developer.email, buyer, p.title)


def has_bought(con, title, buyer_id):
    cursor = con.cursor()
    p = get_product_detail(con, title)
    sql = "select * from {0} where pid={1} and buyer_uid={2}".format(ORDERS_TABLE, p.pid, buyer_id)
    cursor.execute(sql)
    result = cursor.fetchone()
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
        PRODUCTS_TABLE, p.title, p.dev_uid, p.description, p.price,
        get_category_id(con, p.c_func, CATEGORY_FUNCTION_TABLE),
        get_category_id(con, p.c_ui, CATEGORY_UI_STYLE_TABLE))
    execute_non_query(con, sql)
    p = get_product_detail(con, p.title)
    return p.pid


def update_product(con, p, old_title):
    sql = "update {0} set title='{1}' , price={2}, description='{3}' , c_function={4}, c_ui_style={5} where title='{6}'".format(
        PRODUCTS_TABLE, p.title, p.price, p.description, get_category_id(con, p.c_func, CATEGORY_FUNCTION_TABLE),
        get_category_id(con, p.c_ui, CATEGORY_UI_STYLE_TABLE), old_title)
    execute_non_query(con, sql)
    p = get_product_detail(con, p.title)
    return p.pid


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
    if 'SERVER_SOFTWARE' in os.environ:
        from sae.storage import Bucket

        bucket = Bucket('domain1')
        bucket.put_object(filename, file1)
        url = bucket.generate_url(filename)
    else:
        url = filename
        file_full_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.environ.get('USER') == 'Lily':
            file_full_path = "/Users/Lily/PycharmProjects/EIA/static/upload/" + filename
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


def send_mail(to_addrs, buyer, product_title):
    thread1 = SendEmailThread(to_addrs, buyer, product_title)
    thread1.start()


def add_category_item(con, title, type):
    if type == 'c_func':
        table_name = CATEGORY_FUNCTION_TABLE
    elif type == 'c_ui':
        table_name = CATEGORY_UI_STYLE_TABLE
    else:
        return
    sql = "insert into {0} (title) values ('{1}') ".format(table_name, title)
    execute_non_query(con, sql)


def delete_category_item(con, title, type):
    if type == 'c_func':
        table_name = CATEGORY_FUNCTION_TABLE
    elif type == 'c_ui':
        table_name = CATEGORY_UI_STYLE_TABLE
    else:
        return
    sql = "delete from {0} where title='{1}' ".format(table_name, title)
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