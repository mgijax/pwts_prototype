"""
Blueprint for all 'tr' tracking record views
"""
# pylint: disable=invalid-name
from flask import Blueprint

# Define the blueprint for all the views in this directory
blueprint = Blueprint('client', __name__, url_prefix='/client')
