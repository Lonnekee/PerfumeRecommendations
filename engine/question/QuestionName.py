from engine.question.Question import Question
from engine.question.QuestionType import QuestionType as qt


class QuestionName(Question):
    def __init__(self, q_id, question, engine, id_next, perfumes):
        super().__init__(q_id, question, qt.STRING, engine, id_next, [], [], perfumes)

    def set_answer(self, value):
        print("Not setting answer in QuestionText")
