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
    searchForm = TRSearchForm(request.args)
    
    
    # TODO (kstone): Loading search form options via API
    searchForm.priority.choices = gen_vocab_choices(Priority)
    searchForm.size.choices = gen_vocab_choices(Size)
    searchForm.status.choices = gen_vocab_choices(Status)
    
    return render_template("tr_search.html",
        title="TR Search",
        form=searchForm
    )
    
    
# Helpers
def gen_vocab_choices(cvClass):
    """
    Generate option choices for controlled vocab class (cvClass)
    
    only return active terms
    """
    values = cvClass.query \
        .filter_by(active=True) \
        .all()
    choices = [(x.name, x.name) for x in values]
    return choices
    
    
