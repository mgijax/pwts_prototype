"""
    PWTS app configuration
"""
# pylint: disable=invalid-name
# pylint: disable=wrong-import-position
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import flask
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
import jinja2
from flask.ext.sqlalchemy import SQLAlchemy
#import flask_login
#from flask.ext.login import LoginManager, current_user
from pwts.login import login_util
# from mgipython.model.mgd.mgi import MGIUser


# configuration from environment
PG_SERVER = os.environ["PG_SERVER"]
CUR_DBSERVER = PG_SERVER
PG_DBNAME = os.environ["PG_DBNAME"]
CUR_DBNAME = PG_DBNAME
PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
APP_PREFIX = os.environ["APP_PREFIX"]
LOG_DIR = os.environ["LOG_DIR"]

# application object
app = Flask(__name__, static_path="%s/static"%APP_PREFIX)

# set all constants defined above this line to the app.config object
app.config.from_object(__name__)
# load any specific settings for this environment (e.g. prod/dev/test)
app.config.from_envvar("APP_CONFIG_FILE")

# reset any overrides
APP_PREFIX = app.config['APP_PREFIX']


# open up global logger so we can fine tune the individual handlers
app.logger.setLevel(logging.DEBUG)


# configure logging when not in debug mode
if 'WRITE_APP_LOG' in app.config and app.config['WRITE_APP_LOG']:
    
    # make a file logger that rotates every day
    file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, "app.log"),
                                when='D',
                                interval=1,
                                backupCount=14)
    
    
    # set the logging level for the app log
    logLevel = logging.WARNING
    if 'LOG_LEVEL' in app.config:
        logLevelConfig = app.config['LOG_LEVEL'].lower()
        if logLevelConfig == 'debug':
            logLevel = logging.DEBUG
        elif logLevelConfig == 'info':
            logLevel = logging.INFO
        elif logLevelConfig == 'warn' or logLevel == 'warning':
            logLevel = logging.WARNING
        elif logLevelConfig == 'error':
            logLevel = logging.ERROR
        
    file_handler.setLevel(logLevel)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s] - %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    
    @app.before_request
    def log_requests():
        """
        Log only access requests
        """
        app.logger.info("ACCESS - \"%s\"" % request.path)
        
        
# testing postgres dburi
dburi = "postgresql+psycopg2://%s:%s@%s/%s"%(PG_USER, PG_PASS,
	PG_SERVER, PG_DBNAME)

# configure the multiple db binds
# 'mgd' is for mgd 
app.config['SQLALCHEMY_DATABASE_URI'] = dburi
app.config['SQLALCHEMY_BINDS'] = {
	"wts": dburi,
}

# initialise the global db object
#pylint: disable=wrong-import-order
from mgipython import modelconfig
modelconfig.createDatabaseEngineFromApp(app)
db = modelconfig.db


# set the secret key.  keep this really secret:
app.secret_key = 'ThisIsASecretKey;-)'

# prepare the db connections for all requests
@app.before_request
def before_request():
    """
    initialize session before requests
    """
    if 'user' not in session:
        session['user'] = ''
        
    if "NO_DB_COMMIT" in app.config and app.config["NO_DB_COMMIT"]:
        return

    # prevent any database session autoflush
    db.session.autoflush = False
    db.session.close()


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    clean up db connection after requests
    """
    #db.session.rollback()
    
    if "NO_DB_COMMIT" in app.config and app.config["NO_DB_COMMIT"]:
        return

    db.session.commit()
    db.session.expunge_all()
    db.session.close()

# import traceback
# TODO (kstone): add 500 error handler
# @app.errorhandler(500)
# def server_error(e):
#     
#     return render_template('500.html',
#                 error=e,
#                 traceback=traceback), 500

# views
#from forms import *


# create the login manager
#login_manager = LoginManager()
#login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(userid):
#     return MGIUser.query.filter_by(login=userid).first()

# root view
@app.route(APP_PREFIX+'/')
def index():
    """
    Index page
    """
    return render_template('index.html')

    
# @app.route(APP_PREFIX+'/login',methods=['GET','POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us.
#     error=""
#     user=""
#     next=""
#     if request.method=='POST':
#             form = request.form
#             user = 'user' in form and form['user'] or ''    
#             password = 'password' in form and form['password'] or ''
#             next = 'next' in form and form['next'] or ''
#             
#             #get user and log them the heck in
#             userObject = login_util.mgilogin(user, password)
#                 
#             if userObject:
#                     # successful login
#                     session['user']=user
#                     session['password']=password
#                     session['authenticated'] = True
#                     # Login and validate the user.
#                     flask_login.login_user(userObject, remember=True)
#             
#                     flask.flash('Logged in successfully.')
#             
#                     #if not next_is_valid(next):
#                     #    return flask.abort(400)
#             
#                     return flask.redirect(next or flask.url_for('index'))
#                 
#             error = "user or password is invalid"
# 
#     return render_template('authenticate.html',
#             error=error,
#             user=user,
#             next=next
#     )
    
    
# @app.route(APP_PREFIX+'/logout')
# def logout():
#         if session['user']:
#             login_util.mgilogout(session['user'])
#         
#         session['user']=None
#         session['password']=None
#         session['authenticated'] = False
#         
#         flask_login.logout_user()
#         next = flask.request.args.get('next')
#         
#         #if not next_is_valid(next):
#         #    return flask.abort(400)
# 
#         return flask.redirect(next or flask.url_for('index'))
    


#register blueprints
def registerBlueprint(bp):
    """
    Add APP_PREFIX to all blueprints
       so we can use relative names in the code
    """
    url_prefix = APP_PREFIX + bp.url_prefix
    app.register_blueprint(bp, url_prefix=url_prefix)
                           
# API and client blueprints
from pwts.views.api.blueprint import blueprint as apiBlueprint
registerBlueprint(apiBlueprint)

from pwts.views.client.blueprint import blueprint as clientBlueprint
registerBlueprint(clientBlueprint)

# need to turn off autoescaping to allow nested templates inside templatetags
app.jinja_env.autoescape = False

# enable any jinja extensions
# with syntax for template includes
app.jinja_env.add_extension(jinja2.ext.with_)

# initialise any custom jinja global functions and filters
# TODO(kstone): no filters yet


# initialize admin interface
from pwts import admin
admin.initialize(app, db)

#db.session.commit()
db.session.close()

if __name__ == '__main__':
    app.debug = "DEBUG" in os.environ
    app.run(host='mgi-testdb4')
    