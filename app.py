from flask import Flask
from flask_smorest import Api
from resources.store import blp as StoreBlueprint
from resources.items import blp as ItemsBlueprint
from db import db, ItemsModel, StoresModel
from dbconnection.databaseconnect import get_engine
from flask_cors import CORS,cross_origin


def create_app():
    app = Flask(__name__)

    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["DEBUG"] = 1
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/"
    app.config["SQLALCHEMY_DATABASE_URI"] = get_engine()[0]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)
    cors = CORS(app)

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemsBlueprint)

    return [app, db]


if __name__ == '__main__':
    app = create_app()[0]
    app.run(host='0.0.0.0', port=5000)
