from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
from flask.ext.sqlalchemy import SQLAlchemy

import os
import logging

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
app = Flask(__name__,static_path="%s/static"%APP_PREFIX)

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
    from logging.handlers import TimedRotatingFileHandler
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
    
    from flask import request
    @app.before_request
    def log_requests():
        app.logger.info("ACCESS - \"%s\"" % request.path)
        
        
# testing postgres dburi
dburi = "postgresql+psycopg2://%s:%s@%s/%s"%(PG_USER,PG_PASS,
	PG_SERVER,PG_DBNAME)

print dburi

# configure the multiple db binds
# 'mgd' is for mgd 
app.config['SQLALCHEMY_DATABASE_URI'] = dburi
app.config['SQLALCHEMY_BINDS'] = {
	"wts": dburi,
}

# initialise the global db object
from mgipython import modelconfig
modelconfig.createDatabaseEngineFromApp(app)
db = modelconfig.db


# set the secret key.  keep this really secret:
app.secret_key = 'ThisIsASecretKey;-)'

# prepare the db connections for all requests
@app.before_request
def before_request():
    if 'user' not in session:
		session['user'] = ''
        
    # prevent any database session autoflush
    db.session.autoflush = False
    db.session.close()


@app.teardown_appcontext
def shutdown_session(exception=None):
    #db.session.rollback()
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
from login import login_util
import flask_login
from flask.ext.login import LoginManager, current_user
# from mgipython.model.mgd.mgi import MGIUser
import flask

# create the login manager
login_manager = LoginManager()
login_manager.init_app(app)


# prepare the db connections for all requests
@app.before_request
def before_request():
    
#     if current_user and current_user.is_authenticated:
#         session['user'] = current_user.login
#         session['authenticated'] = True
#     
#     if 'user' not in session:
#         session['user'] = ''
#     if 'authenticated' not in session:
#         session['authenticated'] = False
#         
#     if session['user']:
#         login_util.refreshLogin(session['user'])
        
    # prevent any database session autoflush
    db.session.autoflush = False

# @login_manager.user_loader
# def load_user(userid):
#     return MGIUser.query.filter_by(login=userid).first()

# root view
@app.route(APP_PREFIX+'/')
def index():
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
    url_prefix = APP_PREFIX + bp.url_prefix
    app.register_blueprint(bp, url_prefix=url_prefix)
                           
# detail pages
# from views.detail.blueprint import detail as detailBlueprint
# registerBlueprint(detailBlueprint)

# need to turn off autoescaping to allow nested templates inside templatetags
app.jinja_env.autoescape=False

# enable any jinja extensions
import jinja2
# with syntax for template includes
app.jinja_env.add_extension(jinja2.ext.with_)

# initialise any custom jinja global functions and filters
# TODO(kstone): no filters yet

#db.session.commit()
db.session.close()

if __name__ == '__main__':
	app.debug = DEBUG
	app.run(host='mgi-testdb4')