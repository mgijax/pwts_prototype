"""
WTS controlled vocabularies
"""
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
from mgipython.modelconfig import db

class CVMixin(object):
    """
    Mixin for all controlled vocab tables
        with shared columns
    """
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    active = db.Column(db.Boolean)
        
class Area(CVMixin, db.Model):
    __tablename__ = "cv_wts_area"
    
class Category(CVMixin, db.Model):
    __tablename__ = "cv_wts_category"
    email = db.Column(db.String())
    area_key = db.Column(db.Integer, db.ForeignKey("cv_wts_area.key"))
    type_key = db.Column(db.Integer, db.ForeignKey("cv_wts_type.key"))
    status_key = db.Column(db.Integer, db.ForeignKey("cv_wts_status.key"))
    
class Priority(CVMixin, db.Model):
    __tablename__ = "cv_wts_priority"
    
class Size(CVMixin, db.Model):
    __tablename__ = "cv_wts_size"
  
class Status(CVMixin, db.Model):
    __tablename__ = "cv_wts_status"
    
class Type(CVMixin, db.Model):
    __tablename__ = "cv_wts_type"
    

class User(db.Model):
    __tablename__ = "cv_user"
    key = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String())
    active = db.Column(db.Boolean)
    
        