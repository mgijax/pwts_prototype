"""
 Form object for searching TRs
"""
# pylint: disable=too-few-public-methods
from wtforms.form import Form
from wtforms.fields import BooleanField, TextField, SelectMultipleField

class TRSearchForm(Form):
    """
    Define the fields we can search TRs by
    """

    search_string = TextField('TR Title / Description')
    priority = SelectMultipleField('Priority')
    size = SelectMultipleField('Size')
    status = SelectMultipleField('Status')
    requested_by = SelectMultipleField('Requested By')
    assigned_user = SelectMultipleField('Assigned To')
    open = BooleanField('Open TRs Only')


    # TODO (kstone): use WTForms validation framework
    def is_valid(self):
        """
        Returns true is form is valid to search
        """
        fields_empty = True
        for value in self.data.values():
            if value:
                fields_empty = False
                
        if fields_empty:
            return False
            
        return True
