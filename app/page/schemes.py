from marshmallow import Schema, fields


class ThemeSchema(Schema):
    title = fields.Str(required=True)


class ThemeIdSchema(ThemeSchema):
    id = fields.Int()


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeIdSchema, many=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True, required=True)


class QuestionIdSchema(QuestionSchema):
    id = fields.Int()


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionIdSchema, many=True)
