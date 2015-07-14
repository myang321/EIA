from flask import Flask, render_template, redirect, request, session, url_for, g, flash
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
        c_func = db.get_category_function_list(g.db)
        c_ui = db.get_category_ui_style_list(g.db)
        return render_template('index.html', status=status, msg=msg, c_func=c_func, c_ui=c_ui)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        type = request.form['type']
        if type == 'dev':
            result = db.developers_authentication(g.db, username, password)
        elif type == 'buyer':
            result = db.buyers_authentication(g.db, username, password)
        if result != None:
            session['username'] = username
            session['type'] = type
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
        if type == 'dev':
            dev = db.Developer(username, password, email)
            db.add_developer(g.db, dev)
        elif type == 'buyer':
            buyer = db.Buyer(username, password, email)
            db.add_buyer(g.db, buyer)
        return redirect(url_for('index', status=0))
    else:
        return redirect(url_for('index', status=0))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        c_func = request.form['c_func']
        c_ui = request.form['c_ui']
        list1 = db.search_by_category(g.db, c_func, c_ui)
        return render_template('search.html', list1=list1)
    else:
        list1 = db.search_by_category(g.db, 'all', 'all')
        return render_template('search.html', list1=list1)


if __name__ == '__main__':
    app.run()