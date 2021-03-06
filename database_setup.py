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
# For SAE
if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    from sae.storage import Bucket
else:
    from local import *
# table name
DEVELOPERS_TABLE = "developers"
BUYERS_TABLE = "buyers"
PRODUCTS_TABLE = "products"
ORDERS_TABLE = "orders"
IMG_TABLE = "img"
CATEGORY_TABLE = "category"
PRODUCT_CATEGORY_TABLE = "product_category"

# category type
TYPE_C_FUNC = 'c_func'
TYPE_C_UI = 'c_ui'

UPLOAD_FOLDER = 'static/upload/'
ADMIN_PASSWORD = 'eiawestart'


def get_random_number_str():
    return str(randint(1111, 99999999))


class User(object):
    def __init__(self, username, password, email, uid):
        self.username = username
        self.password = password
        self.email = email


class Category(object):
    def __init__(self, cid, title, category_type, description=None):
        self.cid = cid
        self.title = title
        self.type = category_type
        self.description = description


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
                self.img_list = ['/' + UPLOAD_FOLDER + str1 for str1 in self.img_list]
        if self.img_list is None or len(self.img_list) == 0:
            self.img_list = ['/static/img/no_image2.png']

    def get_description(self):
        # print self.description
        str1 = self.description.decode('string_escape')
        str1 = str1.replace('\\', '')
        # print str
        return str1


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

        con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, port=int(MYSQL_PORT))
    else:
        # for local

        print "connecting local mysql"

        con = mdb.connect(host=LOCAL_HOST, user=LOCAL_USERNAME, passwd=LOCAL_PASSWD, db=LOCAL_DB_NAME,
                          port=LOCAL_PORT, charset='utf8')
    return con


def execute_select_one(con, sql):
    cursor = con.cursor()
    try:
        cursor.execute(sql)
    except:
        print "ERROR", sql
        raise
    result = cursor.fetchone()
    return result


def execute_select_all(con, sql):
    cursor = con.cursor()
    try:
        cursor.execute(sql)
    except:
        print "ERROR", sql
        raise
    result = cursor.fetchall()
    return result


def execute_non_query(con, sql):
    cursor = con.cursor()
    try:
        cursor.execute(sql)
    except:
        print "ERROR", sql
        raise
    con.commit()


def user_authentication(con, username, password, user_type):
    es_username = re.escape(username)
    if user_type == 'developer':
        table = DEVELOPERS_TABLE
    elif user_type == 'buyer':
        table = BUYERS_TABLE
    else:
        return
    sql = "select uid,username from {0} where username='{1}' and password='{2}' ".format(table, es_username, password)
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
    if result is None:
        return False
    else:
        return True


def is_dev_email_exist(con, email):
    sql = "select * from developers where email='{0}'".format(email)
    result = execute_select_one(con, sql)
    if result is None:
        return False
    else:
        return True


def is_email_exist(con, email, user_type):
    if user_type == 'dev':
        return is_dev_email_exist(con, email)
    elif user_type == 'buyer':
        return is_buyer_email_exist(con, email)
    return False


def get_category_id(con, title, category_type):
    sql = "select cid from {0} where type='{1}' and title='{2}'".format(CATEGORY_TABLE, category_type, title)
    result = execute_select_one(con, sql)
    return result[0]


def get_category_title(con, pid, category_type):
    sql = "select title from {0} as pc, {1} as c where pid ={2} and c.cid=pc.cid and c.type='{3}' ".format(
        PRODUCT_CATEGORY_TABLE, CATEGORY_TABLE, pid, category_type)
    result = execute_select_one(con, sql)
    if result:
        return result[0]
    return None


def search_by_category(con, c_func, c_ui):
    if c_func == 'all' and c_ui == 'all':
        sql = "select * from {0}".format(PRODUCTS_TABLE)
    elif c_ui == 'all':
        sql = "select * from {0} where pid in ( select pid from {1} where cid={2} )".format(PRODUCTS_TABLE,
                                                                                            PRODUCT_CATEGORY_TABLE,
                                                                                            get_category_id(con, c_func,
                                                                                                            TYPE_C_FUNC))
    elif c_func == 'all':
        sql = "select * from {0} where pid in ( select pid from {1} where cid={2} )".format(PRODUCTS_TABLE,
                                                                                            PRODUCT_CATEGORY_TABLE,
                                                                                            get_category_id(con, c_ui,
                                                                                                            TYPE_C_UI))
    else:
        sql = """
        select * from {0} where pid in(
        select t1.pid from(
         (select * from product_category where cid={1} )
        union all
        (select * from product_category where cid={2} )
        ) as t1 group by t1.pid having count(*)=2)
        """.format(PRODUCTS_TABLE,
                   get_category_id(con, c_func, TYPE_C_FUNC),
                   get_category_id(con, c_ui, TYPE_C_UI))
    result = execute_select_all(con, sql)
    list1 = []
    for row in result:
        product = relation_to_object_mapping_product(con, row)
        list1.append(product)
    return list1


def relation_to_object_mapping_product(con, row):
    pid = row[0]
    print "in relational mapping"
    c_func = get_category_title(con, pid, TYPE_C_FUNC)
    c_ui = get_category_title(con, pid, TYPE_C_UI)
    product = Product(title=row[1], price=row[4], description=row[3],
                      c_func=c_func, c_ui=c_ui, dev_uid=row[2],
                      img_list=get_product_img(con, pid), pid=pid)
    return product


def relation_to_object_mapping_developer(row):
    dev = Developer(uid=row[0], username=row[1], email=row[3])
    return dev


def relation_to_object_mapping_buyer(row):
    buyer = Buyer(uid=row[0], username=row[1], email=row[3])
    return buyer


# def relation_to_object_mapping_category_function(con, row):
#     c_func = CategoryFunction(cid=row[0], title=row[1], description=row[3])
#     return c_func
#
#
# def relation_to_object_mapping_category_ui_style(con, row):
#     c_ui = CategoryUIStyle(cid=row[0], title=row[1], description=row[3])
#     return c_ui


def get_category_value_list(con, category_type):
    sql = "select * from {0} where type='{1}'".format(CATEGORY_TABLE, category_type)
    result = execute_select_all(con, sql)
    # convert to list
    list1 = [Category(cid=row[0], category_type=row[1], title=row[2]) for row in result]
    return list1


def get_product_id(con, title):
    sql = "SELECT pid from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
    result = execute_select_one(con, sql)
    return result[0]


def get_product_detail(con, title):
    sql = "SELECT * from {0} where title='{1}'".format(PRODUCTS_TABLE, title)
    result = execute_select_one(con, sql)
    product = relation_to_object_mapping_product(con, result)
    return product


def get_buyer(con, uid):
    sql = "SELECT * from {0} where uid='{1}'".format(BUYERS_TABLE, uid)
    result = execute_select_one(con, sql)
    buyer = relation_to_object_mapping_buyer(result)
    return buyer


def get_developer(con, uid):
    sql = "SELECT * from {0} where uid='{1}'".format(DEVELOPERS_TABLE, uid)
    result = execute_select_one(con, sql)
    buyer = relation_to_object_mapping_developer(result)
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
    if result is not None:
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
    sql = "insert into {0} (title,dev_uid,description,price) values('{1}',{2},'{3}',{4})".format(
        PRODUCTS_TABLE, p.title, p.dev_uid, p.description, p.price)
    execute_non_query(con, sql)
    pid = get_product_id(con, p.title)
    add_product_category(con, pid, TYPE_C_FUNC, p.c_func)
    add_product_category(con, pid, TYPE_C_UI, p.c_ui)
    return pid


def add_product_category(con, pid, category_type, title):
    cid = get_category_id(con, title, category_type)
    sql = "insert into {0} values ({1},{2})".format(PRODUCT_CATEGORY_TABLE, pid, cid)
    execute_non_query(con, sql)


def delete_product_category(con, pid):
    sql = "delete from {0} where pid ={1}".format(PRODUCT_CATEGORY_TABLE, pid)
    execute_non_query(con, sql)


def delete_img(con, pid, title):
    if 'SERVER_SOFTWARE' in os.environ:
        p = get_product_detail(con, title)
        bucket = Bucket('domain1')
        for url in p.img_list:
            img_name = url.split("/")[-1]
            bucket.delete_object(img_name)
            print "delete bucket object", img_name
    sql = "delete from {0} where pid ={1}".format(IMG_TABLE, pid)
    execute_non_query(con, sql)


def update_product(con, p, old_title):
    sql = "update {0} set title='{1}' , price={2}, description='{3}'  where title='{4}'".format(
        PRODUCTS_TABLE, p.title, p.price, p.description, old_title)
    execute_non_query(con, sql)
    pid = get_product_id(con, p.title)
    delete_product_category(con, pid)
    add_product_category(con, pid, TYPE_C_FUNC, p.c_func)
    add_product_category(con, pid, TYPE_C_UI, p.c_ui)
    return pid


def save_img_url(con, url, pid, is_front):
    sql = "insert into {0} (url,pid,front) values('{1}',{2},{3})".format(IMG_TABLE, url, pid, is_front)
    execute_non_query(con, sql)


def save_image(con, file1, pid, is_front):
    if file1.filename == '':
        return
    # filename = str(pid) + '_' + get_random_number_str() + '_' + file1.filename
    ext = file1.filename.split('.')[-1]
    filename = str(pid) + get_random_number_str() + '.' + ext
    if 'SERVER_SOFTWARE' in os.environ:
        bucket = Bucket('domain1')
        bucket.put_object(filename, file1)
        url = bucket.generate_url(filename)
    else:
        url = filename
        file_full_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.environ.get('USER') == 'Lily':
            file_full_path = "/Users/Lily/PycharmProjects/EIA/static/upload/" + filename
        file1.save(file_full_path)
    save_img_url(con, url, pid, 1 if is_front else 0)


def get_product_img(con, pid):
    sql = "select url from {0} where pid={1} order by front desc".format(IMG_TABLE, pid)
    result = execute_select_all(con, sql)
    list1 = [row[0] for row in result]
    return list1


def delete_product(con, p_title):
    pid = get_product_id(con, p_title)
    delete_product_category(con, pid)
    delete_img(con, pid, p_title)
    sql = "delete from {0} where title='{1}'".format(PRODUCTS_TABLE, p_title)
    execute_non_query(con, sql)


def send_mail(to_addrs, buyer, product_title):
    thread1 = SendEmailThread(to_addrs, buyer, product_title)
    thread1.start()


def add_category_item(con, title, category_type):
    sql = "insert into {0} (type,title) values('{1}','{2}') ".format(CATEGORY_TABLE, category_type, title)
    execute_non_query(con, sql)


def delete_category_item(con, title, category_type):
    sql = "delete from {0} where title='{1}' and type='{2}' ".format(CATEGORY_TABLE, title, category_type)
    execute_non_query(con, sql)


if __name__ == "__main__":
    con1 = conn()
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
    r = get_buyer_orders(con1, 1)
    print r
    # u = Developer("ha", "123", "sadsaa@dasda.com")
