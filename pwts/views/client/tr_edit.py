"""
    Displays TR detail information
"""
from flask import render_template, request
from pwts.views.client.blueprint import blueprint
from pwts.forms.tr_edit import TREditForm
from pwts.model.cv import Priority, Size, Status, User
from pwts.views.client import ChoiceLoader

# Routes


@blueprint.route('/tr/new')
def new_tr():
    """
    page for creating a new TR
    """
    new_tr_form = TREditForm(request.args)
    
    # TODO (kstone): Loading search form options via API
    new_tr_form.priority.choices = ChoiceLoader.gen_vocab_choices(Priority)
    new_tr_form.size.choices = ChoiceLoader.gen_vocab_choices(Size)
    new_tr_form.status.choices = ChoiceLoader.gen_vocab_choices(Status)
    
    user_choices = ChoiceLoader.gen_user_choices()
    new_tr_form.requested_by.choices = user_choices
    new_tr_form.assigned_user.choices = user_choices
    
    # set defaults
    new_tr_form.status.data = 'new'
    new_tr_form.priority.data = 'unknown'
    new_tr_form.size.data = 'unknown'
    
    
    return render_template("tr_new.html",
        title="New TR",
        form=new_tr_form
    )
    
    
# Helpers

    
    
