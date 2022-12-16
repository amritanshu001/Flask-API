import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db, ItemsModel, StoresModel

blp = Blueprint("Items", __name__, description="Operations on Items")


@blp.route("/items/<string:id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, id):
        pass
        # if id not in items:
        #     abort(404, message="Item Not Found")
        # return items[id]

    def delete(self, id):
        pass
        # if id not in items:
        #     abort(404, message="Item not found")
        # del items[id]
        # return {"message": "Item Deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, id):
        pass
        # if id not in items:
        #     abort(404, message="Item not found")
        # if (not item_data["price"] and not item_data["name"]):
        #     abort(404, message="name and price cannot be blank")
        # items[id] = {**item_data, "id": id}
        # return items[id]


@blp.route("/items")
class ItemsMassOps(MethodView):
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        id = item_data["store_id"]
        store = StoresModel.query.filter_by(id=id).first()
        if not store:
            abort(404, message="Store does not exist")
        item = ItemsModel()
        item.item_name = item_data["item_name"]
        item.price = item_data["price"]
        item.stores.append(store)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as i:
            abort(500, message="{}".format(i))
        except SQLAlchemyError as err:
            abort(500, message="{}".format(err))
        else:
            return item

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemsModel.query.all()
        return items
