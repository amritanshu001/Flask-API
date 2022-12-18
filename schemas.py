from marshmallow import Schema, fields


class ItemSchemaSimple(Schema):
    id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    price = fields.Decimal(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Decimal()
    store_id = fields.Int()


class StoreSchemaSimple(Schema):
    id = fields.Str(dump_only=True)
    store_name = fields.Str(required=True)


class StoreUpdateSchema(Schema):
    store_name = fields.Str(required=True)


class ItemSchema(ItemSchemaSimple):
    store_id = fields.Int(required=True, load_only=True)
    stores = fields.List(fields.Nested(StoreSchemaSimple(), dump_only=True))


class StoreSchema(StoreSchemaSimple):
    items = fields.List(fields.Nested(ItemSchemaSimple(), dump_only=True))
