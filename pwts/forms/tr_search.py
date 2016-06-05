"""
 Form object for searching TRs
"""
from wtforms.form import Form
from wtforms.fields import *
from wtforms.widgets import *

class TRSearchForm(Form):

        search_string = TextField('TR Title')
        priority = SelectMultipleField('Priority')
        size = SelectMultipleField('Size')
        status = SelectMultipleField('Status')
