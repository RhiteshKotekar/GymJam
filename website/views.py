from flask import Blueprint, render_template, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)
import mysql.connector as s

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/account")
def account():
    if 'loggedin' in session and session['loggedin']:
        # Retrieve the logged-in user's username from the session
        co = s.connect(host="localhost", user="root", password="ENDr", database='info', auth_plugin='mysql_native_password')
        cu = co.cursor()
        username = session['username']
        query = 'SELECT username, email FROM members WHERE username = %s'
        cu.execute(query, (username,))
        username = cu.fetchone()
        
    return render_template("account.html", username=username)


@views.route('/arms')
def arms():
    return render_template("arms.html")

@views.route('/legs')
def legs():
    return render_template("legs.html")

@views.route('/core')
def core():
    return render_template("core.html")


@views.route('/yoga')
def yoga():
    return render_template("yoga.html")
