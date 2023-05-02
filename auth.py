from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import json
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fyproject_user:7QMbmgPI18cRIsmXrHgXdzSQt0PcIxb5@dpg-ch8cf0g2qv2864s908eg-a.oregon-postgres.render.com/fyproject'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)
import pandas as pd
import csv
import datetime
def get_glassdoor_jobs():
    with open("glassdoor.json",'r') as f:
        
        return json.loads(f.read())

def get_naukri_jobs():
    with open("data/naukri_scraped_data.csv", 'r') as f:
        reader = csv.reader(f)
        return [{"title":row[0],"company":row[1],"salary":row[5],"location":row[6],"url":row[-1]} for row in reader]
    
def get_jooble_jobs():
    with open("jooble.json","r") as f:
        return json.loads(f.read())['jobs']

def get_news():
    with open("news.json","r") as f:
        return json.loads(f.read())


app.secret_key='asdsdfsdfs13sdf_df%&'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)

class UserApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    job_title = db.Column(db.String(120), nullable=False)
    job_url = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    date_applied = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        company = request.form.get('company')
        if company == "naukri":
            data = get_naukri_jobs()[1:]
            print(data)
            return render_template("naukri.html",jobs=data)
        if company == "glassdoor":
            data = get_glassdoor_jobs()
            # print(data)
            return render_template("index.html",jobs=data)
        if company == "jooble":
            data = get_jooble_jobs()
            # print(data)
            return render_template("jooble.html",jobs=data)
    return render_template("index.html",jobs=get_glassdoor_jobs())

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        fullname = firstname + " " + lastname
        user =User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html',error=True)
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html',email_error=True)
        user = User(username=username, email=email, password=password, fullname=fullname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return f"Invalid Credentials"

    return render_template('login.html')

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/applied", methods=['GET','POST'])
def applied():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        company = request.form.get('company')
        job_title = request.form.get('job_title')
        job_url = request.form.get('url')
        location = request.form.get('location')
        status = 'visited'
        date_applied = str(datetime.datetime.today())
        user = UserApplication(username=session['username'],company=company,job_title=job_title,job_url=job_url,location=location,status=status,date_applied=date_applied)
        db.session.add(user)
        db.session.commit()
        return redirect(job_url)
    user = UserApplication.query.filter_by(username=session['username']).all()
    return render_template('applied.html',jobs=user)

@app.route("/update",methods=["POST"])
def update():
    id = request.form.get("job_id")
    status = request.form.get("status")
    user = UserApplication.query.filter_by(id=id).first()
    user.status = status
    db.session.commit()
    return redirect(url_for('applied'))

@app.route("/news")
def news():
    data = get_news()['news']['news']
    return render_template("news.html",data=data)

if __name__ == '__main__':
    app.run(debug=True)