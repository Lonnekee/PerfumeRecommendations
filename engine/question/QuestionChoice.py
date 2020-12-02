from engine.question.Question import Question


# TODO Single select multiple choice or multi select multiple choice.
class QuestionChoice(Question):
    def __init__(self, q_id, question, q_type, engine, id_next, labels, value, perfumes, answer_options):
        super().__init__(q_id, question, q_type, engine, id_next, labels, value, perfumes)
        self.answers = answer_options

    def set_answer(self, answer):
        print("Setting answer QuestionChoice: ", answer)

        # Update the rankings only if we've got possible answers, labels and corresponding values
        if isinstance(self.value, list) and answer < len(self.value) and \
                isinstance(self.labels, list) and answer < len(self.labels):
            print("Updating rankings.")
            data = self.perfumes

            label = self.labels[answer]
            print("  Searching for ", label)

            print("  ")
            rows = (data['Tags'].str.contains(label))
            data[rows]['rank'] += float(self.value[answer])
            # TODO test if this really works
        else:
            print("Not updating rankings.")
