# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'mysecret'
#db.init_app(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
admin = Admin(app)

from app import views, models
from app.models import User, Subscriber, Contact, Service

class UserView(ModelView):
    column_searchable_list = ['username', 'email']
    form_columns = ['username', 'email', 'password_hash']
admin.add_view(UserView(models.User, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class SubscriberView(ModelView):
    column_searchable_list = ['email']
    form_columns = ['email']
admin.add_view(SubscriberView(Subscriber, db.session))

class ContactView(ModelView):
    column_searchable_list = ['name', 'email']
    form_columns = ['name', 'phone', 'email', 'message']
admin.add_view(ContactView(Contact, db.session))

class ServiceView(ModelView):
    column_searchable_list = ['title', 'description']
    form_columns = ['title', 'description']
admin.add_view(ServiceView(Service, db.session))