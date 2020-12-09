from engine.question.Question import Question


# TODO Single select multiple choice or multi select multiple choice.
class QuestionChoice(Question):
    def __init__(self, q_id, question, q_type, engine, id_next, labels, value, perfumes, answer_options):
        super().__init__(q_id, question, q_type, engine, id_next, labels, value, perfumes)
        self.answers = answer_options

    def _update_ranks(self, label, value):
        data = self.perfumes

        # Select all perfumes that contain the relevant label
        print("  Searching for ", label)
        rows = data['Tags'].str.contains(label)

        # Add the value specified for this label
        data.loc[rows, ['rank']] += float(value)
