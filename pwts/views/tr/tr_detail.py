"""
    Displays TR detail information
"""
import json
from pwts.views.tr.blueprint import blueprint
from pwts.model.wts import TrackRec

# Routes
@blueprint.route('/detail/json/<int:key>')
@blueprint.route('/detail/json/tr<int:key>')
@blueprint.route('/detail/json/TR<int:key>')
def tr_detail_json(key):
    """
    return JSON with TR details
    """
    trackrec = TrackRec.query.filter_by(key=key).first()
    if trackrec:
        return render_tr_json(trackrec)

    return json.dumps({"error":"No TR exists with number %d" % key})
    
    
# Helpers

def render_tr_json(trackrec):
    """
    build json response
    """
    
    response = {
        "key": trackrec.key,
        "title": trackrec.tr_title,
        "priority_key": trackrec.priority_key,
        "priority": trackrec.priority.name,
        "size_key": trackrec.size_key,
        "size": trackrec.size.name,
        "status_key": trackrec.status_key,
        "status": trackrec.status.name,
        "description": trackrec.description,
        "progress_notes": trackrec.progress_notes,
        
        "locked_user_key": trackrec.locked_user_key,
        "locked_date": fmt_date(trackrec.locked_date),
        
        "has_directory": trackrec.has_directory,
        "attention_by": fmt_date(trackrec.attention_by),
        "creation_date": fmt_date(trackrec.creation_date),
        "modification_date": fmt_date(trackrec.modification_date)
    }
    
    
    
    return json.dumps(response)
    
    
def fmt_date(datetime):
    """
    display datetime in json
    """
    return datetime and str(datetime) or None
