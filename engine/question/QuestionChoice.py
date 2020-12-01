from engine.question.Question import Question


# TODO Single select multiple choice or multi select multiple choice.
class QuestionChoice(Question):
    def __init__(self, q_id, question, q_type, engine, id_next, value, answer_options):
        super().__init__(q_id, question, q_type, engine, id_next, value)
        self.answers = answer_options

    # value should be an integer
    def set_answer(self, answer_index):
        next_q = self.id_next[answer_index]
        self.engine.set_next_question(int(next_q))

        # if self.value != None:
        #     pass # TODO upvote or downvote relevant perfumes
