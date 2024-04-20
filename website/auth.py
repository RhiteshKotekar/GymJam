
import email
import csv
import mysql.connector as s
co=s.connect(host="localhost", user="root", password="ENDr",database='info',auth_plugin='mysql_native_password')
cu=co.cursor()
from flask_login import current_user, logout_user

from flask import Blueprint, redirect, render_template, request, flash, url_for, session


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        cu.execute("use info")
        q=("select * from members where username='{}'").format(username)
        cu.execute(q)
        t=cu.fetchall()
        q1=("select password from members where username='{}' and password='{}'").format(username,password)
        cu.execute(q1)
        v=cu.fetchall()
        q2=("select email from members where username='{}' and email='{}'").format(username,email)
        cu.execute(q2)
        y=cu.fetchall()
    
        
        if len(email) < 5:
            flash("Username must be greater than 5 characters", category='error')
        elif len(username) < 5:
            flash("Username must be greater than 5 characters", category='error')
        elif len(password) < 5:
            flash("Password must be greater than 5 characters", category='error')
        elif t != []:
            if v != [] and y != []:
                flash("Logged in successfully", category='success')
                session['loggedin'] = True
                session['username'] = username
                return render_template("home.html")
            else:
                flash("Username or Password entered is wrong. Please retry", category='error')


        elif t==[]:
            flash("No acc with mentioned Username found. Please try again or sign up", category='error')
    
    return render_template("login.html")



@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        Username = request.form.get('Username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4 :
            flash('Email must be greater than 3 characters.', category='error')
        elif len(Username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password must be greater than 5 characters.', category='error')
        else:
            flash('Account created!', category='success')
            return render_template("home.html")

        cu.execute("use info")
        q='insert into members values("{}","{}","{}")'.format(Username,email,password1)
        cu.execute(q)
        co.commit()
    return render_template("sign_up.html")

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



@auth.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        L = []
        feedback = request.form.get('feedback')
        if 'loggedin' in session and session['loggedin']:
            username = session['username']
            with open('feedbacks.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                L.append([username, feedback])
                print(L)
                writer.writerows(L)
            flash("Feedback saved, Thank you!", category='success')
            return render_template("home.html")
    return render_template("feedback.html ")


'''
IN HTML
    so make a text area first then add a button so weh you click the button it posts the data using the class to a 
    variable in py.forms get and most method 
IN PY
    you get the data into a variable using get method and then open a csv file use the sidd thing to get the current user 
    and use the syntax on of writer.writerows([username,feedback]) 


'''