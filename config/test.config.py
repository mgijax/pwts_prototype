# Configuration for acceptance tests

# All tests assume no prefix (e.g. root url is /)
APP_PREFIX=''

DEBUG = False
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

LOG_LEVEL = "ERROR"

# remove password requirement for login
DEV_LOGINS = True
