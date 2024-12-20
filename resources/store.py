import uuid

from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import stores

blp = Blueprint("stores", __name__, description="Operations on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            stores.pop(store_id)
            return {f'message":f"Item {store_id} Deleted Successfully', 200}
        except KeyError:
            abort(404, message="Store Does Not Exists")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        try:
            return {"stores": list(stores.values())}
        except KeyError:
            abort(404, message="Store Not Found")

    def post(self):
        store_data = request.get_json()

        if "name" not in store_data:
            abort(
                400,
                message="Bad request. Ensure 'name' is included in the JSON payload.",
            )
        for store in stores.values():
            if (store["name"] == store_data["name"]):
                abort(403, messgae="Store ALready Exists")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
