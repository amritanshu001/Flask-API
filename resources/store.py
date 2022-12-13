import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("Stores", __name__, description="Operations on Store")


@blp.route("/stores/<string:id>")
class Store(MethodView):
    def get(self, id):
        if id not in stores:
            abort(404, message="Store Not Found")
        return stores[id], 200

    def put(self, id):
        if id not in stores:
            abort(404, message="Store not found")
        store_data = request.get_json()
        stores[id] = {**store_data, "id": id}
        return {"message": "Store Changed"}

    def delete(self, id):
        if id not in stores:
            abort(404, message="Store not found")
        del stores[id]
        return {"message": "Store Deleted"}


@blp.route("/stores")
class StoreMassOps(MethodView):
    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        stores[store_id] = {**store_data, "id": store_id}
        return {"id": store_id}

    def get(self):
        return {"stores": list(stores.values())}, 200
