from flask import Flask, render_template, request, redirect, url_for, session

from project import app, queries, connect
import mysql.connector
import re
import bcrypt
from datetime import datetime

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your_secret_key'

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

dbconn = None
connection = None
def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, port=connect.dbport, \
    database=connect.dbname, autocommit=True)
    dbconn=connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("home.html", title="homepage")

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        user_password = request.form['password']
        # Check if account exists 
        dbconn = getCursor()
        dbconn.execute(queries.login(), (email,))
        # Fetch one record and return result
        user = dbconn.fetchone()
        if user is not None:
            db_password = user[3]
            if bcrypt.checkpw(user_password.encode('utf-8'),db_password.encode('utf-8')):
            # If user exists in Users table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = user[0]
                session['role_id'] = user[4]
                # Redirect to member page   
                return redirect(url_for('dashboard'))
            else:
                # password incorrect
                msg = 'Incorrect password! Try again.'
        else:
            # user doesnt exist or email incorrect
            msg = 'Incorrect email'
    # Show the login form with message (id any)
    return render_template('login.html',title="login", msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('role_id', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists
        dbconn = getCursor()
        dbconn.execute(queries.login(), (email,))
        user = dbconn.fetchone()
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # user doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print(hashed)
            dbconn.execute(queries.register(), (username, hashed, email, 2, ))
            msg = 'You have successfully registered!'
        print(msg)   
        return render_template('login.html',title="login", msg=msg)
    # Show registration form with message (if any)
    return render_template('login.html', title="login", msg=msg)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")