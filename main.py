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
@app.route('/')
def index(status=0, msg=None):
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html', status=status, msg=msg)


@app.route('/login')
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


@app.route('/signup')
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


if __name__ == '__main__':
    app.run()
