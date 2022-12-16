from flask_sqlalchemy import SQLAlchemy as sql

db = sql()

store_item = db.Table('store_item',
                      db.Column('store_id', db.Integer, db.ForeignKey(
                          'stores.id'), primary_key=True),
                      db.Column('item_id', db.Integer, db.ForeignKey(
                          'items.id'), primary_key=True)
                      )


class StoresModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(60), nullable=False, unique=True)
    items = db.relationship(
        'ItemsModel', secondary=store_item, back_populates="stores")

    def __repr__(self):
        return f'<Store {self.store_name}>'


class ItemsModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(60), nullable=False, unique=True)
    price = db.Column(db.Float)
    stores = db.relationship(
        'StoresModel', secondary=store_item, back_populates="items")

    def __repr__(self):
        return f'<Item {self.item_name}>'
