import uuid

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import items, stores

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()

        if ("price" not in item_data
                or "store_id" not in item_data
                or "name" not in item_data):
            abort(401, message="Item Data Does not contain any one of the price,store_id,name")

        for item in items:
            if (item["store_id"] == item_data["store_id"] and item["name"] == item_data["name"]):
                abort(401, message="Item ALready Exists")

        if item_data["store_id"] not in stores:
            abort(404, message="Store Not Present")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def put(self,item_id):
        item_data = request.get_json()

        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
            )
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
