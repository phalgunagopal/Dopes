from flask import Blueprint, render_template,request,flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET' ,'POST'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first() 
        print(user)
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in SUCCESSFULLY", category="succcess")
                login_user(user,remember=True)
                return redirect(url_for('views.home', user=current_user))
            else:
                flash("Incorrect Password", category="error")
        else:
            flash("User Doesnt Exist...", category="error")        
    return render_template("index.html")

@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method=="POST":
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists...', category='error')
        elif len(email)<4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName)<2:
            flash('First name must be greater than 1 character.', category='error')
        
        elif len(password1)<5:
            flash('Password must be at least 5 characters.', category='error')
        elif password1!=password2:
            flash('Passwords don\'t match.', category='error')
        
        else:
            new_user=User(email=email,firstname=firstName,lastname=lastName,username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("ACCOUNT CREATED!",category="success")
            login_user(new_user,remember=True)
            return redirect(url_for("views.home"))
    # if request.method=="GET":
    #     new_user = User(email=email, first_name=first_name, password=generate_password_hash(
    #             password1, method='sha256'))
    #     db.session.add(new_user)
    #     db.session.commit()
    #     login_user(new_user, remember=True)
    #     flash('Account created!', category='success')
    #     return redirect(url_for('views.home'))
     
    return render_template("signup.html",user=current_user)

  