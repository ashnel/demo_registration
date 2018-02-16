from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import md5
emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')
app = Flask(__name__)  
app.secret_key = 'supertopsecret'
mysql = MySQLConnector(app, 'wall')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def fieldcheck():
	goto = '/'
	email = request.form['email']
	db_email = mysql.query_db("SELECT email FROM users WHERE email = '{}'".format(email))
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
		elif len(db_email) > 0:
			flash("This user already exists!", 'color')
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
				session['id']=mysql.query_db('SELECT id FROM users WHERE users.email ="{}"'.format(email))
				return redirect('/wall')
			else:
				flash('Your email and password do not match. Please try again.', 'color')
		return redirect(goto)

@app.route('/message', methods=['POST'])
def post_message():
	posted_message = request.form['postbox']
	user_id = session['id'][0]['id']
	query = mysql.query_db("INSERT INTO `wall`.`messages` (message, user_id, created_at, updated_at) VALUE ('{}', '{}', NOW(), NOW())".format(posted_message, user_id))
	return redirect('/wall')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/wall')
def render_wall():
	query = mysql.query_db("SELECT * FROM messages")
	messages = query
	post_query = mysql.query_db("SELECT users.first_name, users.last_name, messages.message, messages.id, messages.created_at FROM messages JOIN users on messages.user_id = users.id")
	comment_query = mysql.query_db("SELECT users.first_name, users.last_name, comments.comment, comments.message_id, comments.created_at FROM comments JOIN users on users.id = comments.user_id JOIN messages on messages.user_id = users.id GROUP BY comments.id ORDER BY comments.created_at DESC")
	return render_template('wall.html', all_messages=post_query, all_comments=comment_query)

@app.route('/comment/<id>', methods=['POST'])
def post_comment(id):
	posted_comment = request.form['commentbox']
	user_id = session['id'][0]['id']
	query = "INSERT INTO comments (comment, user_id, message_id, created_at, updated_at) VALUE (:comment, :id, :specific_id, NOW(), NOW())"
	data = {'comment': request.form['commentbox'], 'id': user_id, 'specific_id': id}
	mysql.query_db(query, data)
	return redirect('/wall')

app.run(debug=True)