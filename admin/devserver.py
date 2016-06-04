import sys,os.path
# adjust the path for running the tests locally, so that it can find app (i.e. 1 dirs up)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import os
import socket

# set development config environment
rootDir = os.environ['PWTS']
os.environ['APP_CONFIG_FILE'] = os.path.join(rootDir, 'config', 'dev.config.py')
from pwts import app

hostname=socket.gethostname()


serverPort = int(os.environ["DEV_SERVER_PORT"])
app.run(debug=True,host=hostname,port=serverPort)
