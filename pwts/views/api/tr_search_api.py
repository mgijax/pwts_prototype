"""
API for searching TRs by various fields
"""
from flask import abort, jsonify, request, url_for
from pwts.views.api.blueprint import blueprint
from pwts.model.cv import Priority, Size, Status
from pwts.model.wts import TrackRec
from pwts import app, db
from pwts.forms.tr_search import TRSearchForm

# Routes
    
@blueprint.route('/tr/search', methods=['GET'])
def search_trs():
    """
    return JSON with found track records
    """
    
    search_form = TRSearchForm(request.args)
    
    trackrecs = query_trackrecs(search_form)

    return render_results_json(trackrecs)


# Helpers

def query_trackrecs(search_form):
    """
    search database for trackrecs
       using arguments in TRSearchForm search_form
    """
    
    query = TrackRec.query
    
    if search_form.priority.data:
        priorities = search_form.priority.data
        sub_query = gen_cv_subquery(priorities, Priority)
        query = query.filter(sub_query.exists())
        
    if search_form.size.data:
        sizes = search_form.size.data
        sub_query = gen_cv_subquery(sizes, Size)
        query = query.filter(sub_query.exists())
    
    if search_form.status.data:
        statuses = search_form.status.data
        sub_query = gen_cv_subquery(statuses, Status)
        query = query.filter(sub_query.exists())
    
    if search_form.search_string.data:
        search = search_form.search_string.data.lower()
        search = "%" + search + "%"
        query_part1 = query.filter(db.func.lower(TrackRec.title).like(search))
        query_part2 = query.filter(db.func.lower(TrackRec.description).like(search))
        
        query = query_part1.union(query_part2)
        
    query = query.order_by(TrackRec.key)
    return query.all()


def gen_cv_subquery(values, cv_class):
    """
    Generate a subquery for a controlled vocab table (cv_class)
        to be used in exists clause
        
    all values are search case-insensitive
    cvClass must implement CVMixin
        (which provides name column)
    """
    values = [v.lower() for v in values]
    cv_alias = db.aliased(cv_class)
    tr_alias = db.aliased(TrackRec)
    sub_query = db.session.query(tr_alias) \
        .join(cv_alias) \
        .filter(db.func.lower(cv_alias.name).in_(values)) \
        .filter(tr_alias.key == TrackRec.key) \
        .correlate(TrackRec)
    return sub_query

def render_results_json(trackrecs):
    """
    build json response for trackrecs
    """
    
    response_objects = []
    for trackrec in trackrecs:
            
        url = url_for('client.tr_detail', key=trackrec.key)
                
        response_objects.append({
            "key": trackrec.key,
            "title": trackrec.title,
            "priority_key": trackrec.priority_key,
            "priority": trackrec.priority and trackrec.priority.name or '',
            "size_key": trackrec.size_key,
            "size": trackrec.size and trackrec.size.name or '',
            "status_key": trackrec.status_key,
            "status": trackrec.status and trackrec.status.name or '',
        
            "locked_user_key": trackrec.locked_user_key,
            "locked_date": fmt_date(trackrec.locked_date),
        
            "creation_date": fmt_date(trackrec.creation_date),
            "modification_date": fmt_date(trackrec.modification_date),
            "url": url
        })
    
    response = {
        "trackrecs": response_objects
    }
    return jsonify(response)
    
    
def fmt_date(datetime):
    """
    display datetime in json
    """
    return datetime and datetime.strftime("%Y-%m-%d %H:%M:%S") or None
