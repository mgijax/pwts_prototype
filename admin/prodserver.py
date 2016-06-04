import sys,os.path
# adjust the path for running the tests locally, so that it can find app (i.e. 1 dirs up)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import cherrypy
import os
import socket

# set production config environment
rootDir = os.environ['PWTS']
os.environ['APP_CONFIG_FILE'] = os.path.join(rootDir, 'config', 'prod.config.py')

from pwts import app

hostname=socket.gethostname()

serverPort = int(os.environ["SERVER_PORT"])

# cherrypy config
cherrypy.tree.graft(app, '/')
cherrypy.config.update({
    'server.socket_host': hostname,
    'server.socket_port': serverPort,
    'engine.autoreload.on': False
})

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()
    
