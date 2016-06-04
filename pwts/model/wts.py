"""
Core WTS tables
"""
from mgipython.modelconfig import db
from cv import *

class TrackRec(db.Model):
    __tablename__="wts_trackrec"
    key = db.Column(db.Integer, primary_key=True)
    priority_key = db.Column(db.Integer, db.ForeignKey("cv_wts_priority.key"))
    size_key = db.Column(db.Integer, 
                         db.ForeignKey("cv_wts_size.key"),
                         index=True)
    status_key = db.Column(db.Integer, 
                         db.ForeignKey("cv_wts_status.key"),
                         index=True)
    status_user_key = db.Column(db.Integer, 
                         db.ForeignKey("cv_user.key"),
                         index=True)
    status_set_date = db.Column(db.DateTime())
    locked_user_key = db.Column(db.Integer, 
                         db.ForeignKey("cv_user.key"),
                         index=True)
    locked_date = db.Column(db.DateTime())
    tr_title = db.Column(db.String())
    has_directory = db.Column(db.Boolean)
    attention_by = db.Column(db.DateTime())
    creation_date = db.Column(db.DateTime())
    modification_date = db.Column(db.DateTime())
    
    description = db.Column(db.String())
    progress_notes = db.Column(db.String())
    
    
    priority = db.relationship("Priority",
                               uselist=False,
                               backref="trs")
    status = db.relationship("Status",
                             uselist=False,
                             backref="trs")
    
    areas = db.relationship("TR_Area",
                            backref="trs")
    
    types = db.relationship("TR_Type",
                            backref="trs")
    
    assignedUsers = db.relationship("TR_AssignedUser")
    
    requestedBy = db.relationship("TR_RequestedUser")
    
    statusChanges = db.relationship("StatusHistory")
    
    

class TR_Area(db.Model):
    __tablename__="wts_tr_area"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    area_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_wts_area.key"),
                        index=True,
                        primary_key=True)
        
class TR_Type(db.Model):
    __tablename__="wts_tr_type"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    area_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_wts_area.key"),
                        index=True,
                        primary_key=True)
    
class TR_AssignedUser(db.Model):
    __tablename__="wts_tr_assign_user"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    user_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_user.key"),
                        index=True,
                        primary_key=True)
    
class TR_RequestedUser(db.Model):
    __tablename__="wts_tr_request_user"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    user_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_user.key"),
                        index=True,
                        primary_key=True)
    
        

class StatusHistory(db.Model):
    __tablename__="wts_status_history"
    key = db.Column(db.Integer, primary_key=True)
    tr_key = db.Column(db.Integer, 
                       db.ForeignKey("wts_trackrec.key"),
                       index=True)
    status_key = db.Column(db.Integer, 
                         db.ForeignKey("cv_wts_status.key"),
                         index=True)
    user_key = db.Column(db.Integer, 
                         db.ForeignKey("cv_user.key"),
                         index=True)
    set_date = db.Column(db.DateTime())
    
    
class WTSRelationship(db.Model):
    __tablename__ = "wts_relationship"
    tr_key = db.Column(db.Integer, 
                   db.ForeignKey("wts_trackrec.key"),
                   primary_key=True)
    related_tr_key = db.Column(db.Integer, 
                   db.ForeignKey("wts_trackrec.key"),
                   primary_key=True)

    transitive_closure = db.Column(db.Boolean, primary_key=True)
    
        