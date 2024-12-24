from marshmallow import Schema, fields



class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(dump_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class StoreSchema(PlainStoreSchema):
    items =  fields.List(fields.Nested(ItemSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(),dump_only=True))




class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)


class TagandItemSchema(Schema):
    message = fields.Str()
    items = fields.Nested(ItemSchema)
    tags = fields.Nested(TagSchema)






