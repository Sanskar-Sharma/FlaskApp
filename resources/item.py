import uuid

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, item_data):


        for item in items:
            if (item["store_id"] == item_data["store_id"] and item["name"] == item_data["name"]):
                abort(401, message="Item ALready Exists")


        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):

        try:
            item: object = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item Not Found")

    def delete(self,item_id):
        try:
            items.pop(item_id)
            return {f'message":f"Item {item_id} Deleted Successfully', 200}
        except KeyError:
            abort(404, message="Item Does Not Exists")
