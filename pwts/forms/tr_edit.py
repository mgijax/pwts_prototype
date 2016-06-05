"""
 Form object for creating/editting TRs
"""
# pylint: disable=too-few-public-methods
from wtforms.form import Form
from wtforms.fields import BooleanField, HiddenField, TextField, SelectField, SelectMultipleField

class TREditForm(Form):
    """
    Define the fields we can edits TRs by
    """
    
    title = TextField('Title')
    priority = SelectField('Priority')
    size = SelectField('Size')
    status = SelectField('Status')
    requested_by = SelectMultipleField('Requested By')
    assigned_user = SelectMultipleField('Assigned To')
    
    key = HiddenField("TrackRec.key")

