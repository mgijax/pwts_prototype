"""
 Form object for searching TRs
"""
# pylint: disable=too-few-public-methods
from wtforms.form import Form
from wtforms.fields import TextField, SelectMultipleField

class TRSearchForm(Form):
    """
    Define the fields we can search TRs by
    """

    search_string = TextField('TR Title / Description')
    priority = SelectMultipleField('Priority')
    size = SelectMultipleField('Size')
    status = SelectMultipleField('Status')
