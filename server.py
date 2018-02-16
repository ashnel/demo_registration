from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import md5
emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')
app = Flask(__name__)  
app.secret_key = 'supertopsecret'
mysql = MySQLConnector(app, 'registration')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def fieldcheck():
	goto = '/'
	if request.form['formtype'] == 'register':
		if len(request.form['email']) < 1:
			flash('Email field cannot be empty.', 'color')
		elif not emailregex.match(request.form['email']):
			flash('Invalid Email address', 'color')
		elif len(request.form['firstname']) < 1:
			flash('First Name field cannot be empty.', 'color')
		elif not nameregex.match(request.form['firstname']):
			flash('First Name must be alphabetical characters only.', 'color')
		elif len(request.form['lastname']) < 1:
			flash('Last Name field cannot be empty.', 'color')
		elif not nameregex.match(request.form['lastname']):
			flash('Last Name must be alphabetical characters only.', 'color')
		elif len(request.form['password']) < 9:
			flash('Password must be more than 8 Characters!', 'color')
		elif len(request.form['passwordcheck']) < 9:
			flash('Password must be more than 8 Characters!', 'color')
		elif request.form['password'] != request.form['passwordcheck']:
			flash('Password does not match password confirmation!', 'color')
		else:
			password = md5.new(request.form['password']).hexdigest()
			first_name = request.form['firstname']
			last_name = request.form['lastname']
			email = request.form['email']
			user_query = ('INSERT INTO users (first_name, last_name, password, email, created_at, updated_at) VALUES ("{}", "{}", "{}", "{}", NOW(), NOW())'.format(first_name, last_name, password, email))
			mysql.query_db(user_query)
			return render_template('success.html', regEmail = email)
		return redirect(goto)
	elif request.form['formtype'] == 'login': # Login
		if len (request.form['email']) < 1:
			flash("Email field cannot be empty.", 'color')
		elif not emailregex.match(request.form['email']):
			flash('Invalid Email address', 'color')
		elif len(request.form['password']) < 1:
			flash("Password field cannot be empty.", 'color')
		else:
			email = request.form['email']
			password = md5.new(request.form['password']).hexdigest()
			db_password = mysql.query_db("SELECT password FROM users WHERE email = '{}'".format(email))
			db_email = mysql.query_db("SELECT email FROM users WHERE email = '{}'".format(email))
			if len(db_password) < 1 and len(db_email) < 1:
				flash('Not a registered user. Please register or try again.', 'color')
			elif email == db_email[0]['email'] and password == db_password[0]['password']:
				return render_template('logged_in.html', regEmail = email)
			else:
				flash('Your email and password do not match. Please try again.', 'color')
		return redirect(goto)
app.run(debug=True)