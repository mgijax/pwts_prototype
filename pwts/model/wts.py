"""
Core WTS tables
"""
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
from mgipython.modelconfig import db
#from pwts.model.cv import *
    

class TRAreaAssoc(db.Model):
    __tablename__ = "wts_tr_area"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    area_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_wts_area.key"),
                        index=True,
                        primary_key=True)
        
class TRTypeAssoc(db.Model):
    __tablename__ = "wts_tr_type"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    type_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_wts_type.key"),
                        index=True,
                        primary_key=True)
    
class TRAssignedUserAssoc(db.Model):
    __tablename__ = "wts_tr_assign_user"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    user_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_user.key"),
                        index=True,
                        primary_key=True)
    
class TRRequestedUserAssoc(db.Model):
    __tablename__ = "wts_tr_request_user"
    tr_key = db.Column(db.Integer, 
                        db.ForeignKey("wts_trackrec.key"),
                        index=True,
                        primary_key=True)
    user_key = db.Column(db.Integer, 
                        db.ForeignKey("cv_user.key"),
                        index=True,
                        primary_key=True)
    
        

class StatusHistory(db.Model):
    __tablename__ = "wts_status_history"
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
    
    
class TrackRecChildAssoc(db.Model):
    __tablename__ = "wts_trackrec_child"
    tr_key = db.Column(db.Integer, 
                   db.ForeignKey("wts_trackrec.key"),
                   primary_key=True)
    child_tr_key = db.Column(db.Integer, 
                   db.ForeignKey("wts_trackrec.key"),
                   primary_key=True)
    
    
class TrackRec(db.Model):
    __tablename__ = "wts_trackrec"
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
    title = db.Column(db.String())
    has_directory = db.Column(db.Boolean)
    attention_by = db.Column(db.DateTime())
    creation_date = db.Column(db.DateTime(),
                        default=db.func.now())
    modification_date = db.Column(db.DateTime(),
                        default=db.func.now())
    
    description = db.Column(db.String())
    progress_notes = db.Column(db.String())
    
    
    priority = db.relationship("Priority",
                               uselist=False,
                               backref="trs")
    size = db.relationship("Size",
                             uselist=False,
                             backref="trs")
    status = db.relationship("Status",
                             uselist=False,
                             backref="trs")
    
    areas = db.relationship("Area",
                            secondary=TRAreaAssoc.__table__,
                            backref="trs")
    
    types = db.relationship("Type",
                            secondary=TRTypeAssoc.__table__,
                            backref="trs")
    
    assigned_users = db.relationship("User",
                                    secondary=TRAssignedUserAssoc.__table__)
    
    requested_by = db.relationship("User",
                                  secondary=TRRequestedUserAssoc.__table__)
    
    statusChanges = db.relationship("StatusHistory")
    
    child_trs = db.relationship("TrackRec",
                                secondary=TrackRecChildAssoc.__table__,
                                primaryjoin="TrackRec.key==TrackRecChildAssoc.tr_key",
                                secondaryjoin="TrackRec.key==TrackRecChildAssoc.child_tr_key",
                                backref=db.backref("parent", uselist=False))
    
        