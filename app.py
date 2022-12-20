from flask import Flask
from flask_smorest import Api
from resources.store import blp as StoreBlueprint
from resources.items import blp as ItemsBlueprint
from resources.user_management import blp as UsersBlueprint
from db import db, ItemsModel, StoresModel
from dbconnection.databaseconnect import get_engine
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dbconnection.redis_connect import blocklist_connection


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
    app.config["SECRET_KEY"] = "justanotherkey"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=0.5)

    db.init_app(app)
    api = Api(app)
    cors = CORS(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = blocklist_connection.get(jti)
        return token_in_redis is not None

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(UsersBlueprint)

    return [app, db]


if __name__ == '__main__':
    app = create_app()[0]
    app.run(host='0.0.0.0', port=5000)
