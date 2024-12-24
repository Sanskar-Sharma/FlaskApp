from db import db

class ItemTags(db.Model):
    __tablename__ = "item_tags"

    id = db.Column(db.Integer,unique= True)
    item_id =  db.Column(db.Integer(),db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer(),db.ForeignKey("stores.id"))