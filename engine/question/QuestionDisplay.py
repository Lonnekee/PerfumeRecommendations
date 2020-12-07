from engine.question.QuestionChoice import QuestionChoice
from engine.question.QuestionType import QuestionType as qt


class QuestionDisplay(QuestionChoice):

    def __init__(self, q_id, question, engine, id_next, labels, value, perfumes, answer_options):
        super().__init__(q_id,
                         question,
                         qt.CHOICE_DISPLAY,
                         engine,
                         id_next,
                         labels,
                         value,
                         perfumes,
                         answer_options)

