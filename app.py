from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
import os
import math
from datetime import datetime
# import flask_mysqldb
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
# import sqlite3
# connection=sqlite3.connect("Project8.db")
# cursor=connection.cursor()
# cursor.execute("insert into Verification(Username,Password) values('rahul1','rahul')")
# cursor.execute("insert into Verification(Username,Password) values('rahul2','rahul')") 
# cursor.execute("insert into Verification(Username,Password) values('rahul3','rahul')")
# connection.commit()
# import mysql.connector as connector

# class User:
#     def __init__(self,id,User,Pass,Email):
#         self.id = id
#         self.User = User
#         self.Pass = Pass
#         self.Email = Email

#     def __repr__(self):
#         return f'<User: {self.User}>'

# users = []

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__,template_folder="Templates",static_folder="static")
app.secret_key = 'rahul'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'user-system'
  
# mysql = MySQL(app)
  

class Register(db.Model):
    Sno = db.Column(db.Integer)
    id = db.Column(db.Integer,primary_key=True, nullable=False)
    Email = db.Column(db.String(21), nullable=False)
    User = db.Column(db.String(21), nullable=False)
    Pass = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    


class Contact(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), nullable=False)
    EmailAddress = db.Column(db.String(21), nullable=False)
    MobileNumber = db.Column(db.String(12), nullable=False)
    Query = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)


# @app.route("/", methods = ['GET', 'POST'])
# def Register():
#     if(request.method=='POST'):
#         id = request.form.get('id')
#         username = request.form.get('User')
#         password = request.form.get('Pass')
#         email = request.form.get('Email')
#         # entry = Register(id = id,User=username,Pass=password,Email = Email,Date=datetime.now())
#         # db.session.add(entry)
#         # db.session.commit()
#         users.append(User(id,username,password,email))
#         return render_template('Home.html', params=params)
#     return render_template('index.html')

# @app.before_request
# def before_request():
#     g.user = None

#     if 'user_id' in session:
#         user = [x for x in users if x.id == session['user_id']][0]
#         g.user = user
        

# @app.route("/", methods = ['GET', 'POST'])
# def login():
#     if ('user' in session and session['user'] == params['admin_user']):
#         posts = Posts.query.all()
#         return render_template('login.html', params=params)


#     if request.method=='POST':
#         username = request.form.get('username')
#         userpass = request.form.get('password')
#         if username == params['admin-user'] and userpass == params['admin-password']:
#             #set the session variable
#             session['user'] = username
#             posts = Posts.query.all()
#             return render_template('Home.html', params=params)

#     return render_template('login.html', params=params)

 
@app.route("/")
def register():
    return render_template('index.html', params=params)




database={'root':'password','username':'password','rahul':'rahul','admin':'password','tenkati':'tenkati'}

@app.route('/signin',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
	    return render_template('index.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('index.html',info='Invalid Password')
        else:
	         return render_template('Home.html',name=name1)









# @app.route("/signin",methods = ['GET'])
# def Signin():
#     mydb=connector.connect(host="localhost",
#     user="root",
#     password="",
#     database="learncoding")
#     mycur=mydb.cursor()
#     if request.method=='POST':
#         result=request.form
#         Username1 = result['Username']  
#         Password1 = result['Password']
#         mycur.execute("select Sno,Username,Emailaddress,Password from register where Username='"+Username1+"'AND Password='"+Password1+"'")
#         c=mycur.fetchall()   
#         mydb.commit()
#         mycur.close()
#         count=mycur.rowcount
#         if count==1:
#             return render_template('Home.html')
#         else:
#             return render_template('Signin.html')
#     mydb.commit()
#     mycur.close()


@app.route("/Home")
def Home():
    # if not g.user:
    #     return redirect(url_for('login'))
    return render_template('Home.html')


@app.route("/About")
def about():
    return render_template('About.html', params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        Username = request.form.get('Username')
        EmailAddress = request.form.get('EmailAddress')
        MobileNumber = request.form.get('MobileNumber')
        Query = request.form.get('Query')
        entry = Contact(Username=Username,EmailAddress=EmailAddress, MobileNumber=MobileNumber,Query=Query,Date= datetime.now())
        db.session.add(entry)
        db.session.commit()
        # mail.send_message('New message from ' + Username,
        #                   sender=EmailAddress,
        #                   recipients = [params['gmail-user']],
        #                   body = Query + "\n" + MobileNumber
        #                   )
    return render_template('Contact.html', params=params)


@app.route("/Purchase")
def purchase():
    return render_template('Purchase.html', params=params)



# @app.route('/logout')
# def logout():
#     session.pop('User')
#     return redirect('/Signin')

if __name__ =='__main__':
    app.run(debug=True)