"""
    Displays TR detail information
"""
from flask import render_template, request
from pwts.views.client.blueprint import blueprint
from pwts.forms.tr_search import TRSearchForm
from pwts.model.cv import Priority, Size, Status, User
from pwts.views.client import ChoiceLoader

# Routes


@blueprint.route('/tr/search')
def tr_search_page():
    """
    TR search HTML page
    """
    search_form = TRSearchForm(request.args)
    
    
    # TODO (kstone): Loading search form options via API
    search_form.priority.choices = ChoiceLoader.gen_vocab_choices(Priority)
    search_form.size.choices = ChoiceLoader.gen_vocab_choices(Size)
    search_form.status.choices = ChoiceLoader.gen_vocab_choices(Status)
    
    user_choices = ChoiceLoader.gen_user_choices()
    search_form.requested_by.choices = user_choices
    search_form.assigned_user.choices = user_choices
    
    return render_template("tr_search.html",
        title="TR Search",
        form=search_form
    )
    
    
# Helpers

    
    
