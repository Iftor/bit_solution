from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        theme_list = list(
            filter(
                lambda theme: theme.title.lower() == title.lower(),
                self.app.database.themes
            )
        )
        return theme_list[0] if theme_list else None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        theme_list = list(
            filter(
                lambda theme: theme.id == id_,
                self.app.database.themes
            )
        )
        return theme_list[0] if theme_list else None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        question_list = list(
            filter(
                lambda question: question.title.lower() == title.lower(),
                self.app.database.questions
            )
        )
        return question_list[0] if question_list else None

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = Question(
            id=self.app.database.next_question_id,
            title=str(title),
            theme_id=theme_id,
            answers=answers
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        return self.app.database.questions