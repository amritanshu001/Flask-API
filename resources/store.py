import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, StoreUpdateSchema


blp = Blueprint("Stores", __name__, description="Operations on Store")


@blp.route("/stores/<string:id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, id):
        if id not in stores:
            abort(404, message="Store Not Found")
        return stores[id], 200

    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, store_data, id):
        if id not in stores:
            abort(404, message="Store not found")
        stores[id] = {**store_data, "id": id}
        return {"message": "Store Changed"}

    def delete(self, id):
        if id not in stores:
            abort(404, message="Store not found")
        del stores[id]
        return {"message": "Store Deleted"}


@blp.route("/stores")
class StoreMassOps(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, message="Store Name Already Exists")
        store_id = uuid.uuid4().hex
        stores[store_id] = {**store_data, "id": store_id}
        return stores[store_id]

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
