"""
Blueprint for all REST api routes
"""
# pylint: disable=invalid-name
from flask import Blueprint

# Define the blueprint for all the views in this directory
blueprint = Blueprint('api', __name__, url_prefix='/api')
