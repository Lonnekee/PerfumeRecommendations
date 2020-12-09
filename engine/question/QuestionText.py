from engine.question.Question import Question
from engine.question.QuestionType import QuestionType as qt


class QuestionText(Question):
    def __init__(self, q_id, question, engine, id_next, perfumes):
        super().__init__(q_id, question, qt.STRING, engine, id_next, [], [], perfumes)

    def set_answer(self, value):
        self.engine.add_additional_info("budget", value)  # TODO hardcoded budget for now
