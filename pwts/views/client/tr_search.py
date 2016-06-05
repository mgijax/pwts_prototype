"""
    Displays TR detail information
"""
from flask import render_template, request
from pwts.views.client.blueprint import blueprint
from pwts.forms.tr_search import TRSearchForm
from pwts.model.cv import Priority, Size, Status

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
    return choices
    
    
