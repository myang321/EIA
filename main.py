from flask import Flask, render_template, redirect, request, session, url_for, g

import database_setup as db

app = Flask(__name__)
app.debug = True
app.secret_key = 'F12Zr47j3yXR~X@H!jmM]Lwf/,?KT'


@app.before_request
def before_request():
    g.db = db.conn()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# status=0 normal
# status=1 signup open
# status=2 login open
@app.route('/', methods=['GET', 'POST'])
def index(status=0, msg=None):
    if request.method == 'POST':
        pass
    else:
        c_func = db.get_category_value_list(g.db, db.TYPE_C_FUNC)
        c_ui = db.get_category_value_list(g.db, db.TYPE_C_UI)
        return render_template('index.html', status=status, msg=msg, c_func=c_func, c_ui=c_ui)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        type = request.form['type']
        if type == 'developer':
            result = db.developers_authentication(g.db, username, password)
        elif type == 'buyer':
            result = db.buyers_authentication(g.db, username, password)
        if result != None:
            session['username'] = username
            session['type'] = type
            session['uid'] = result[0]
            return redirect(url_for('index', status=0))
        else:
            return redirect(url_for('index', status=2))
    else:
        return redirect(url_for('index', status=0))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        type = request.form['type']
        if db.is_email_exist(g.db, email, type):
            msg = "email already used"
            return redirect(url_for('index', status=1, msg=msg))
        if type == 'developer':
            dev = db.Developer(username, password, email)
            db.add_developer(g.db, dev)
            result = db.developers_authentication(g.db, username, password)
        elif type == 'buyer':
            buyer = db.Buyer(username, password, email)
            db.add_buyer(g.db, buyer)
            result = db.buyers_authentication(g.db, username, password)
        session['username'] = username
        session['type'] = type
        session['uid'] = result[0]
        return redirect(url_for('index', status=0))
    else:
        return redirect(url_for('index', status=0))


@app.route('/search', methods=['GET'])
def search():
    c_func = request.args['c_func']
    c_ui = request.args['c_ui']
    list1 = db.search_by_category(g.db, c_func, c_ui)
    editable = False
    return render_template('search.html', list1=list1, editable=editable)


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/developer/')
def developer():
    list1 = db.get_developers_products(g.db, session['uid'])
    list2 = db.get_developer_orders(g.db, session['uid'])
    c_func = db.get_category_value_list(g.db, db.TYPE_C_FUNC)
    c_ui = db.get_category_value_list(g.db, db.TYPE_C_UI)
    editable = True
    p = db.Product()
    is_new = True
    return render_template('developer.html', list1=list1, list2=list2, c_func=c_func, c_ui=c_ui, editable=editable, p=p,
                           is_new=is_new)


@app.route('/buyer/')
def buyer():
    list1 = db.get_buyer_orders(g.db, session['uid'])
    editable = False
    return render_template('buyer.html', list1=list1, editable=editable)


@app.route('/product_detail/')
def product_detail():
    title = request.args.get('title')
    product = db.get_product_detail(g.db, title)
    if session.get('uid') == None:
        bought = False
    else:
        bought = db.has_bought(g.db, title, session['uid'])
    return render_template('product_detail.html', p=product, bought=bought)


@app.route('/buy/', methods=['POST'])
def buy():
    product_title = request.form['p_title']
    db.create_order(g.db, product_title, session['uid'])
    return redirect(url_for('product_detail', title=product_title))


@app.route('/upload/', methods=['POST'])
def upload_product():
    product_title = request.form['title']
    price = request.form['price']
    description = request.form['description']
    c_func = request.form['c_func']
    c_ui = request.form['c_ui']
    is_new = request.form['is_new']
    old_title = request.form.get('old_title')
    product = db.Product(product_title, price, description, c_func, c_ui, session['uid'])
    if is_new == "True":
        pid = db.save_product(g.db, product)
    else:
        pid = db.update_product(g.db, product, old_title)
    front_img = request.files.get('front_img')
    detail_img_list = request.files.getlist('detail_img')
    db.save_image(g.db, front_img, pid, True)
    for f in detail_img_list:
        db.save_image(g.db, f, pid, False)
    return redirect(url_for('developer'))


@app.route('/edit_product/', methods=['GET', 'POST'])
def edit_product():
    if request.method == 'POST':
        pass
    else:
        p_title = request.args.get('p_title')
        product = db.get_product_detail(g.db, p_title)
        c_func = db.get_category_value_list(g.db, db.TYPE_C_FUNC)
        c_ui = db.get_category_value_list(g.db, db.TYPE_C_UI)
        is_new = False
        return render_template('edit_product.html', p=product, c_func=c_func, c_ui=c_ui, is_new=is_new)


@app.route('/delete_product/', methods=['POST'])
def delete_product():
    product_title = request.form['p_title']
    db.delete_product(g.db, product_title)
    return redirect(url_for('developer'))


@app.route('/admin/category', methods=['GET'])
def admin_category():
    print session.get('admin'), session.get('admin') != 1
    if session.get('admin') != 1:
        print "redirect(url_for('admin_auth'))"
        return redirect(url_for('admin_auth'))
    c_func = db.get_category_value_list(g.db, db.TYPE_C_FUNC)
    c_ui = db.get_category_value_list(g.db, db.TYPE_C_UI)
    return render_template('admin_category.html', c_func=c_func, c_ui=c_ui)


@app.route('/admin/add_category_item', methods=['POST'])
def admin_add_category_item():
    if session.get('admin') != 1:
        redirect(url_for('admin_auth'))
    type = request.form['type']
    title = request.form['title']
    db.add_category_item(g.db, title, type)
    return redirect(url_for('admin_category'))


@app.route('/admin/delete_category_item', methods=['POST'])
def admin_delete_category_item():
    if session.get('admin') != 1:
        redirect(url_for('admin_auth'))
    type = request.form['type']
    title = request.form['title']
    db.delete_category_item(g.db, title, type)
    return redirect(url_for('admin_category'))


@app.route('/admin/auth', methods=['POST', 'GET'])
def admin_auth():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == db.ADMIN_PASSWORD:
            session['admin'] = 1
            return redirect(url_for('admin_category'))
        return render_template('admin_login_fail.html')
    else:
        return render_template('admin_auth.html')


if __name__ == '__main__':
    app.run()
