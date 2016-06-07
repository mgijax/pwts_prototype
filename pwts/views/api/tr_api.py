"""
    REST API for TrackRec objects
"""
from flask import abort, jsonify, request, url_for
from pwts.views.api.blueprint import blueprint
from pwts.model.wts import TrackRec
from pwts.model.cv import Priority, Size, Status, User
from pwts import db, app

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
        
    trackrec = build_new_tr()
    edit_tr(trackrec, request.json)
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
    
    child_trs = []
    for child_tr in trackrec.child_trs:
        child_trs.append({
            "key": child_tr.key,
            "url": url_for('client.tr_detail', key=child_tr.key)
        })
        
    requested_by = [user.login for user in trackrec.requested_by]
    requested_by.sort()

    assigned_users = [user.login for user in trackrec.assigned_users]
    assigned_users.sort()
    
    
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
        
        "areas": [area.name for area in trackrec.areas],
        "requested_by": requested_by,
        "assigned_users": assigned_users,
        
        "child_trs": child_trs
    }
    
    
    
    return jsonify(response)


def build_new_tr():
    """
    Create a new TR
    """
         
    trackrec = TrackRec()
    trackrec.key = db.session.query(db.func.max(TrackRec.key).label("max_key")) \
        .one().max_key + 1
        
    return trackrec

def edit_tr(trackrec, data):
    """
    Set TR with values from data
    """
    
    trackrec.title = data['title']
    
    if 'description' in data and data['description']:
        trackrec.description = data['description']
        
    if 'progress_notes' in data and data['progress_notes']:
        trackrec.progress_notes = data['progress_notes']
    
    if 'priority' in data and data['priority']:
        trackrec.priority = Priority.query.filter_by(name=data['priority']).first()    
    
    if 'size' in data and data['size']:
        trackrec.size = Size.query.filter_by(name=data['size']).first()
        
    if 'status' in data and data['status']:
        trackrec.status = Status.query.filter_by(name=data['status']).first()
        
    if 'requested_by' in data and data['requested_by']:
        app.logger.debug("hello rqb = %s" % data['requested_by'])
        trackrec.requested_by = User.query.filter(User.login.in_(data['requested_by'])).all()
        
    if 'assigned_user' in data and data['assigned_user']:
        trackrec.assigned_users = User.query.filter(User.login.in_(data['assigned_user'])).all()
        
    
def fmt_date(datetime):
    """
    display datetime in json
    """
    return datetime and datetime.strftime("%Y-%m-%d %H:%M:%S") or None
