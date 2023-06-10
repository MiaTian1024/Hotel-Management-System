from flask import Flask, render_template, request, abort, redirect, url_for, session
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import json
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from project import app, queries, connect
import mysql.connector
import re
import bcrypt
from datetime import datetime

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your_secret_key'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
with open(client_secrets_file) as file:
    data = json.load(file)
GOOGLE_CLIENT_ID = data['web']['client_id']

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

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
    dbconn = getCursor()
    dbconn.execute(queries.roomInfo())
    roomInfo = dbconn.fetchall()
    return render_template("home.html", title="homepage", roomInfo=roomInfo)

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
                session['name'] = user[1]
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


@app.route("/GoogleLogin")
def GoogleLogin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session['loggedin'] = True
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["picture"] = id_info.get("picture")
    session['role_id'] = 2
    dbconn = getCursor()
    dbconn.execute(queries.googleRegister(), (session['name'],session['role_id']))
    dbconn.execute(queries.googleUser(), (session['name'], ))
    googleUser=dbconn.fetchone()
    session['id'] = googleUser[0]
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.clear()
    # Redirect to login page
    return redirect(url_for('login'))


@app.route("/dashboard")
def dashboard():
    dbconn = getCursor()
    if not session:
        msg = 'Please login first!'
        return render_template('login.html',title="login", msg=msg)
    elif session['role_id'] == 1:  # The role ID for admin is 1
        dbconn.execute(queries.adminInfo(), (session['id'],))
        adminInfo = dbconn.fetchone()
        return render_template("AdminDashboard.html", title="Admin Dashboard", session=session, adminInfo=adminInfo )
    elif session['role_id'] == 2: #The role ID for approval manager is 2
        dbconn.execute(queries.customerInfo(), (session['id'],))
        customerInfo = dbconn.fetchone()
        dbconn.execute(queries.roomInfo())
        roomInfo = dbconn.fetchall()
        return render_template("dashboard.html", title="Dashboard", roomInfo=roomInfo, session=session, customerInfo=customerInfo )
    elif session["name"]:
        dbconn.execute(queries.roomInfo())
        roomInfo = dbconn.fetchall()
        return render_template("dashboard.html", title="Dashboard", roomInfo=roomInfo, session=session)
    

@app.route("/service")
def service():
    dbconn = getCursor()
    dbconn.execute(queries.service())
    service = dbconn.fetchall()
    return render_template("service.html", title="Services", session=session, service=service)

@app.route("/roomtypes")
def roomtypes():
    dbconn = getCursor()
    dbconn.execute(queries.roomTypes())
    roomtypes = dbconn.fetchall()
    return render_template("roomTypes.html", title="Room Types", session=session, roomtypes=roomtypes)

@app.route("/searchRoom" , methods=["POST"])
def searchRoom():
    typeName=request.form.get('typeName')
    check_in_date=request.form.get('check_in_date')
    check_out_date=request.form.get('check_out_date')
    dbconn = getCursor()
    dbconn.execute(queries.searchRoom(), (typeName, ))
    roomSearch = dbconn.fetchall()
    return render_template("dashboard.html", title="Room Search", typeName=typeName, check_in_date=check_in_date, check_out_date=check_out_date, session=session, roomSearch=roomSearch)

@app.route("/newBooking" , methods=["GET", "POST"])
def newBooking():
    if request.method == 'POST':
       roomType=request.form.get('roomType')
       fullName=request.form.get('fullName')
       phone=request.form.get('phone')
       breakfast=request.form.get('breakfast')
       extraBed=request.form.get('extraBed')
       check_in_date=request.form.get('check_in_date')
       check_out_date=request.form.get('check_out_date')
       status="Pending"
       user_id=session['id']
       print(user_id)
       dbconn=getCursor()
       dbconn.execute(queries.addBooking(), (user_id, fullName, phone, roomType, check_in_date, check_out_date, breakfast, extraBed, status))      
       msg = 'You have successfully booked this room!'
       dbconn.execute(queries.typeInfo(), (roomType, ))
       roomInfo=dbconn.fetchone()  
       dbconn.execute(queries.bookingBill(), (user_id, ))
       billInfo=dbconn.fetchone()        
       return render_template("newBooking.html", msg=msg, title="Booking", billInfo=billInfo, roomInfo=roomInfo, session=session)
    roomtype=request.args.get('type')
    dbconn = getCursor()
    dbconn.execute(queries.typeInfo(), (roomtype, ))
    roomInfo=dbconn.fetchone()
    return render_template("newBooking.html", title="Booking", roomInfo=roomInfo, session=session)

@app.route("/bill")
def bill():
    billId = request.args.get('billId')
    dbconn = getCursor()
    dbconn.execute(queries.billInfo(), (billId, ))
    billInfo = dbconn.fetchone()
    roomPrice=billInfo[5] * billInfo[10]
    dbconn.execute(queries.service())
    service = dbconn.fetchall()
    breakfastPrice=service[0][2] * billInfo[6]
    extraBedPrice=service[1][2] * billInfo[7]
    totalAmount=roomPrice + breakfastPrice + extraBedPrice
    return render_template("bill.html", 
                        title="Bill", 
                        billInfo=billInfo, 
                        service=service, 
                        breakfastPrice=breakfastPrice,  
                        extraBedPrice=extraBedPrice,
                        roomPrice=roomPrice,
                        totalAmount=totalAmount,
                        session=session)

@app.route("/bookings", methods=["GET", "POST"])
def bookings():
    if request.method == 'POST':
         bookingId=request.form.get('bookingId')
         dbconn = getCursor()
         dbconn.execute(queries.billConfirm(), (bookingId,))
         billInfo=dbconn.fetchone()
         dbconn.execute(queries.bookingInfo(), (session['id'],))
         bookingInfo=dbconn.fetchall()
         msg="Thank you for your payment. Your room has been confirmed."
         return render_template("bookings.html", msg=msg, bookingInfo=bookingInfo, billInfo=billInfo, session=session)
    dbconn = getCursor()
    dbconn.execute(queries.bookingInfo(), (session['id'],))
    bookingInfo=dbconn.fetchall()
    return render_template("bookings.html", title="Booking", bookingInfo=bookingInfo, session=session)
   

@app.route("/confirmCancel")
def confirmCancel():
    dbconn = getCursor()
    billId = request.args.get('billId')
    if billId:
        confirmMsg="Are you sure you want to cancel this booking?"    
        dbconn.execute(queries.bookingInfo(), (session['id'],))
        bookingInfo=dbconn.fetchall()
        return render_template("bookings.html", title="Booking", billId=billId, confirmMsg=confirmMsg, bookingInfo=bookingInfo, session=session)

@app.route("/cancelBill")
def cancelBill():
        billId = request.args.get('billId')
        dbconn.execute(queries.billCancel(), (billId, ))
        cancelMsg="You have successfully canceled this booking."
        dbconn.execute(queries.bookingInfo(), (session['id'],))
        bookingInfo=dbconn.fetchall()
        return render_template("bookings.html", title="Booking", cancelMsg=cancelMsg, session=session, bookingInfo=bookingInfo)

