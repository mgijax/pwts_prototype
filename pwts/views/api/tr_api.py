"""
    REST API for TrackRec objects
"""
from flask import abort, jsonify, request
from pwts.views.api.blueprint import blueprint
from pwts.model.wts import TrackRec
from pwts import db

# Routes
    
@blueprint.route('/tr/<int:key>', methods=['GET'])
def get_tr(key):
    """
    return JSON with TR details
    """
    trackrec = TrackRec.query.filter_by(key=key).first()
    if trackrec:
        return render_tr_json(trackrec)

    return jsonify({"error":"No TR exists with number %d" % key}), 404
    
    
@blueprint.route('/tr', methods=['POST'])
def create_tr():
    """
    create a new TR
    """
    if not request.json or not 'title' in request.json:
        abort(400)
    
    # TODO (kstone): flesh out TR creation        
    trackrec = TrackRec()
    trackrec.title = request.json['title']
    trackrec.key = db.session.query(db.func.max(TrackRec.key).label("max_key")) \
        .one().max_key + 1
    db.session.add(trackrec)
    
    return render_tr_json(trackrec), 201
    
    
@blueprint.route('/tr/<int:key>', methods=['PUT'])
def update_tr(key):
    """
    Update a TR
    """
    trackrec = TrackRec.query.filter_by(key=key).first()
    if not trackrec:
        return jsonify({"error":"No TR exists with number %d" % key}), 404

    if not request.json:
        abort(400)
        
    trackrec.title = request.json['title']

    return render_tr_json(trackrec)
    
    
@blueprint.route('/tr/<int:key>', methods=['DELETE'])
def delete_tr(key):
    """
    Delete a TR
    """
    trackrec = TrackRec.query.filter_by(key=key).first()
    if not trackrec:
        return jsonify({"error":"No TR exists with number %d" % key}), 404
    
    db.session.delete(trackrec)
    
    return jsonify({'result': True})
    
# Helpers

def render_tr_json(trackrec):
    """
    build json response
    """
    
    response = {
        "key": trackrec.key,
        "title": trackrec.title,
        "priority_key": trackrec.priority_key,
        "priority": trackrec.priority and trackrec.priority.name or '',
        "size_key": trackrec.size_key,
        "size": trackrec.size and trackrec.size.name or '',
        "status_key": trackrec.status_key,
        "status": trackrec.status and trackrec.status.name or '',
        "description": trackrec.description,
        "progress_notes": trackrec.progress_notes,
        
        "locked_user_key": trackrec.locked_user_key,
        "locked_date": fmt_date(trackrec.locked_date),
        
        "has_directory": trackrec.has_directory,
        "attention_by": fmt_date(trackrec.attention_by),
        "creation_date": fmt_date(trackrec.creation_date),
        "modification_date": fmt_date(trackrec.modification_date),
        
        "child_trs": ",".join([str(x.key) for x in trackrec.child_trs])
    }
    
    
    
    return jsonify(response)
    
    
def fmt_date(datetime):
    """
    display datetime in json
    """
    return datetime and str(datetime) or None
