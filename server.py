from flask import Flask, render_template, request, redirect, session, flash
import re
emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')
app = Flask(__name__)  
app.secret_key = 'supertopsecret'

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def fieldcheck():
    if len(request.form['email']) < 1:
        flash('Email field cannot be empty.')
    elif not emailregex.match(request.form['email']):
        flash('Invalid Email address')
    elif len(request.form['firstname']) < 1:
        flash('First Name field cannot be empty.')
    elif not nameregex.match(request.form['firstname']):
        flash('First Name must be alphabetical characters only.')
    elif len(request.form['lastname']) < 1:
        flash('Last Name field cannot be empty.')
    elif not nameregex.match(request.form['lastname']):
        flash('Last Name must be alphabetical characters only.')
    elif len(request.form['password1']) < 9:
        flash('Password must be more than 8 Characters!')
    elif len(request.form['password2']) < 9:
        flash('Password must be more than 8 Characters!')
    elif request.form['password1'] != request.form['password2']:
        flash('Password does not match Password confirmation!')
    else:
        flash('Thank you for registering! You should receive a feeling of self-gratification via mail in 12-48 weeks!')
    return redirect('/')
app.run(debug=True)