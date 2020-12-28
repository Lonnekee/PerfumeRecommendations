from engine.question.QuestionChoice import QuestionChoice
from engine.question.QuestionType import QuestionType as qt


class QuestionChoiceMultiple(QuestionChoice):

    def __init__(self, q_id, question, engine, id_next, labels, value, perfumes, answer_options):
        super().__init__(q_id,
                         question,
                         qt.MULTIPLE,
                         engine,
                         id_next,
                         labels,
                         value,
                         perfumes,
                         answer_options)

    def set_answer(self, answer_list):
        print("Setting answer QuestionChoiceMultiple: ", answer_list)

        if not isinstance(answer_list, list):
            print("QuestionChoiceMultiple should receive list of 1's and 0's")
            exit(1)

        for index, a in enumerate(answer_list):
            if a == 1:
                self._update_ranks(self.labels[index], self.value[index], index)