from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash

# User Login and Regstration
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template('registration.html')

# Redirect from this route still pending. Waiting on Dashboard html. ********** UPDATE REDIRECTING ROUT ************
@app.route('/register', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect("/signup")
    email = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email)
    if user_in_db:
        flash("An account is already using that email. Please use another email address.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/user_dash") 

