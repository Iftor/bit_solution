from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import request_schema

from app.quiz.models import Answer
from app.quiz.schemes import (
    ThemeSchema, ThemeListSchema, QuestionSchema, ListQuestionSchema, ThemeIdSchema, QuestionIdSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]

        existing_theme = await self.store.quizzes.get_theme_by_title(title)
        if existing_theme:
            raise HTTPConflict

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeIdSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    async def post(self):
        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers: list[dict] = self.data["answers"]

        existing_question = await self.store.quizzes.get_question_by_title(title)
        if existing_question:
            raise HTTPConflict

        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound

        if len(answers) < 2:
            raise HTTPBadRequest

        correct_answers = list(filter(lambda answer: answer["is_correct"], answers))
        if len(correct_answers) != 1:
            raise HTTPBadRequest

        question = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        return json_response(data=QuestionIdSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    async def get(self):
        questions = await self.store.quizzes.list_questions()
        return json_response(data=ListQuestionSchema().dump({"questions": questions}))
