from engine.question.Question import Question


# TODO Single select multiple choice or multi select multiple choice.
class QuestionChoice(Question):
    def __init__(self, q_id, question, q_type, engine, id_next, value, answer_options):
        super().__init__(q_id, question, q_type, engine, id_next, value)
        self.answers = answer_options

    def set_answer(self, value):
        print("Setting answer QuestionChoice: ", value)
