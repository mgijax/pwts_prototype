"""
    Displays TR detail information
"""
from flask import render_template, request
from pwts.views.client.blueprint import blueprint
from pwts.forms.tr_search import TRSearchForm
from pwts.model.cv import Priority, Size, Status, User

# Routes


@blueprint.route('/tr/search')
def tr_search_page():
    """
    TR search HTML page
    """
    search_form = TRSearchForm(request.args)
    
    
    # TODO (kstone): Loading search form options via API
    search_form.priority.choices = gen_vocab_choices(Priority)
    search_form.size.choices = gen_vocab_choices(Size)
    search_form.status.choices = gen_vocab_choices(Status)
    
    user_choices = gen_user_choices()
    search_form.requested_by.choices = user_choices
    search_form.assigned_user.choices = user_choices
    
    return render_template("tr_search.html",
        title="TR Search",
        form=search_form
    )
    
    
# Helpers
def gen_vocab_choices(cv_class):
    """
    Generate option choices for controlled vocab class (cv_class)
    
    only return active terms
    """
    values = cv_class.query \
        .filter_by(active=True) \
        .all()
    choices = [(x.name, x.name) for x in values]
    choices.sort()
    return choices
    
def gen_user_choices():
    """
    Generate option choices for users
    
    only return active users
    """
    users = User.query \
        .filter_by(active=True) \
        .all()
    choices = [(x.login, x.login) for x in users]
    choices.sort()
    return choices
    
    
