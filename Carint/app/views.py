# app/views.py

from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Subscriber, Contact, Service, Client

@app.route('/')
def home():
    services = Service.query.all()
    clients = Client.query.all()
    return render_template('index.html', services=services, clients = clients)

@app.route('/services')
def services():
    # Tüm servisleri veritabanından al
    services = Service.query.all()
    
    # services.html sayfasına servisleri iletecek şekilde render et
    return render_template('services.html', services=services)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form.get('email')

        if email:
            new_subscriber = Subscriber(email=email)
            db.session.add(new_subscriber)
            db.session.commit()
            flash('Subscription successful!', 'success')
        else:
            flash('Email is required for subscription.', 'danger')

    return redirect(url_for('home'))

@app.route('/contactus', methods=['POST'])
def contactus():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']

        new_contact = Contact(name=name, phone=phone, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('home'))