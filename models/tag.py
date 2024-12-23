
from  db import db

class TagModel(db.Model):

    __table__name = "tags"

    id  = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(80),unique=False,nullable = False)
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"),nullable = False)

    store = db.relationship("StoreModel",bacK_populates = "tags")
