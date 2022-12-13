import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on Items")


@blp.route("/items/<string:id>")
class Items(MethodView):
    def get(self, id):
        if id not in items:
            abort(404, message="Item Not Found")
        return items[id], 200

    def delete(self, id):
        if id not in items:
            abort(404, message="Item not found")
        del items[id]
        return {"message": "Item Deleted"}

    def put(self, id):
        if id not in items:
            abort(404, message="Item not found")
        item_data = request.get_json()
        if (not item_data["price"] and not item_data["name"]):
            abort(404, message="name and price cannot be blank")
        items[id] = {**item_data, "id": id}
        return {"message": "Item Changed"}


@blp.route("/items")
class ItemsMassOps(MethodView):
    @blp.arguments(ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json()
        if item_data["store_id"] not in stores:
            abort(404, message="Store does not exist")
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(400, message="Item Exists")
        item_id = uuid.uuid4().hex
        items[item_id] = {**item_data, "id": item_id}
        return {"id": item_id}

    def get(self):
        return {"items": list(items.values())}, 200
