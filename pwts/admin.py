"""
Set up the Admin interface
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from pwts.model.cv import Area, Category, Priority, \
        Size, Status, Type, User

def initialize(flask_app, flask_db):
    """
    Define the admin views
    """
    admin = Admin(flask_app, name="pwts", template_mode="bootstrap3")
    
    admin.add_view(ModelView(Area, flask_db.session))
    admin.add_view(ModelView(Category, flask_db.session))
    admin.add_view(ModelView(Priority, flask_db.session))
    admin.add_view(ModelView(Size, flask_db.session))
    admin.add_view(ModelView(Status, flask_db.session))
    admin.add_view(ModelView(Type, flask_db.session))
    admin.add_view(ModelView(User, flask_db.session))
    