from flask import Blueprint, render_template, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, SignupForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        flash('Incorrect email or password. Please try again.', category='error')
    return render_template("login.html", user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()

    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password = form.password1.data

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Proceed to login.', category='success')
            return redirect(url_for('auth.login'))  # Redirect to login page

    return render_template("sign_up.html", user=current_user, form=form)

