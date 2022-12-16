import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema, StoreUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db, StoresModel


blp = Blueprint("Stores", __name__, description="Operations on Store")


@blp.route("/stores/<string:id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, id):
        store = StoresModel.query.filter_by(id=id).first()
        if store:
            return store
        else:
            abort(404, message="Store not found")

    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, store_data, id):
        store = StoresModel.query.filter_by(id=id).first()
        if store:
            store.store_name = store_data["store_name"]
            try:
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                abort(404, message="Error {} occured".format(err))
            else:
                return store
        else:
            abort(404, message="Store not found")

    def delete(self, id):
        store = StoresModel.query.filter_by(id=id).first()
        if store:
            try:
                db.session.delete(store)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                abort(404, message="Erorr {} occured".format(err))
            else:
                return {"message": "Store Deleted"}
        else:
            abort(404, message="Store not found")


@blp.route("/stores")
class StoreMassOps(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoresModel(**store_data)

        db.session.add(store)

        try:
            db.session.commit()
        except IntegrityError as i:
            db.session.rollback()
            abort(500, message="{}".format(i))
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, message="{}".format(err))
        else:
            return store

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoresModel.query.all()
        return stores
