import uuid

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, item_data):

        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(501,message = "An error occurred while inserting the item.")

        return item


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        return ItemModel.query.get_or_404(item_id)

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id = item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item





    def delete(self,item_id):
        try:
            item = ItemModel.query.delete(item_id)
            db.session.delete()
            db.session.commit()
            return {f'message":f"Item {item_id} Deleted Successfully', 200}
        except KeyError:
            abort(404, message="Item Does Not Exists")

@blp.route("/item/<string:item_id>/tag/<string:item_id>")
class ItemTag(MethodView):

    def delete(self,item_id):
        pass

