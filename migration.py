from app import create_app
from flask_migrate import Migrate
from db import ItemsModel, StoresModel

[app, db] = create_app()
migrate = Migrate(app, db)
