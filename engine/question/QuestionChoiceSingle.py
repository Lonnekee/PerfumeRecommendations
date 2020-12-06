from engine.question.QuestionChoice import QuestionChoice
from engine.question.QuestionType import QuestionType as qt


class QuestionChoiceSingle(QuestionChoice):

    def __init__(self, q_id, question, engine, id_next, labels, value, perfumes, answer_options):
        super().__init__(q_id,
                         question,
                         qt.CHOICE_SINGLE_SELECT,
                         engine,
                         id_next,
                         labels,
                         value,
                         perfumes,
                         answer_options)

    def set_answer(self, index):
        print("Setting answer QuestionChoiceSingle: ", index)

        # Update the rankings only if we've got possible answers, labels and corresponding values
        if isinstance(self.value, list) and index < len(self.value) and \
                isinstance(self.labels, list) and index < len(self.labels):
            print("Updating rankings.")
            self._update_ranks(self.labels[index], self.value[index])
        else:
            print("Not updating rankings.")