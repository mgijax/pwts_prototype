"""
    Displays TR detail information
"""
from flask import render_template
from pwts.views.client.blueprint import blueprint

# Routes

    

@blueprint.route('/tr/<int:key>')
@blueprint.route('/tr/tr<int:key>')
@blueprint.route('/tr/TR<int:key>')
def tr_detail(key):
    """
    TR detail HTML page
    """
    
    return render_template("tr_detail.html",
                title="TR%d Detail" % key,
                key=key
                )
    
    
