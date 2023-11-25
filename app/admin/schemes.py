from marshmallow import Schema, fields


class AdminBaseSchema(Schema):
    email = fields.Str(required=True)


class AdminRequestSchema(AdminBaseSchema):
    password = fields.Str(required=True)


class AdminResponseSchema(AdminBaseSchema):
    id = fields.Int()
