"""
    Handle logins for the pwi
    
    Setting config value DEV_LOGINS = True
        removes password requirement for all users.
        (User must still exist in MGI_User table)
        
"""
import logging
import os
from flask import session
#from pwts import app


# TODO (kstone): implement logins
# def mgilogin(user, password):
#     """
#     Login functionality for users
#     
#     returns MGIUser object (if successful)
#     """
# 
#     #get user and log them in
#     userObject = None
#     if app.config['DEV_LOGINS']:
#         # For unit tests we don't want to authenticate with Unix passwords
#         #userObject = MGIUser.query.filter_by(login=user).first()
#         # TODO (kstone): use WTS user table
#         pass
#     else:
#         userObject = unixUserLogin(user, password)
#     
#     if userObject:
#         session['user'] = user
#         _createUserLogger(user)
#         app.logger.debug("User Login - %s" % user)
#         
#     return userObject
# 
# 
# 
# def mgilogout(user):
#     """
#     Perform any cleanup necessary for logging out
#     """
#     app.logger.debug("User Logout - %s" % user)
#     _removeUserLogger(user)
#     
    
