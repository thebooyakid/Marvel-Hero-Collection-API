from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_heroes.forms import UserLoginForm, UserSigninForm
from marvel_heroes.models import User, db, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(name, username, email,password)

            user = User(name=name, username=username, email=email, password = password)
            db.session.add(user)
            db.session.commit()

            flash(f"{username}: Your account has been created")
            return redirect(url_for('auth.signin'))
    except:
        raise Exception('Please check forms')
    return render_template('signup.html', form=form)
    
@auth.route('/signin',methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print(username,password)

            logged_user = User.query.filter(User.username == username).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("Login successful:", "auth-success")
                return redirect(url_for('site.profile'))
            else:
                flash("Email/Password incorrect", "auth-failed")
                return redirect(url_for("auth.signin"))
    except:
        raise Exception('Invalid form data: Please check forms')
    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
