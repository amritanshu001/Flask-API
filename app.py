from flask import Flask
from flask_smorest import Api
from resources.store import blp as StoreBlueprint
from resources.items import blp as ItemsBlueprint


app = Flask(__name__)

app.config["PROPOGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "V1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/"

api = Api(app)

api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemsBlueprint)
