from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    username = fields.Str()
    bio = fields.Str()
    specialization = fields.Str()

class CollectionItemSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    category = fields.Str()
    estimated_value = fields.Float()
    acquired_at = fields.DateTime()
    created_at = fields.DateTime()
