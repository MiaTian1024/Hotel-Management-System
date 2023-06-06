from project import app

from flask import render_template
from flask import request, jsonify
from flask import redirect
from flask import url_for

@app.route("/")
def home():
    return render_template("home.html", title="login")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")