# Production (Live) configuration settings
DEBUG = False

SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 10

# write logs to $LOG_DIR/app.log
WRITE_APP_LOG = True

LOG_LEVEL = "INFO"

# remove password requirement for login
DEV_LOGINS = False


# remeber user login for 1 day
from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(1)