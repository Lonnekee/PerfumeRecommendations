from engine.question.Question import Question
from engine.question.QuestionType import QuestionType as qt


class QuestionBudget(Question):
    def __init__(self, q_id, question, engine, id_next, perfumes):
        super().__init__(q_id, question, qt.BUDGET, engine, id_next, [], [], perfumes)

    def set_answer(self, value):
        if not isinstance(value, float):
            print("QuestionNumber should receive a float as an answer.")
            return

        print("Filtering perfumes... only perfumes costing less than %.2lf remain." % value)
        self.exclude = self.perfumes[self.perfumes["Price"] > value].index
        self.include = self.perfumes[self.perfumes["Price"] <= value].index

        self.perfumes.loc[self.exclude, ['included']] = False

        # Store the reason why we updated these perfumes
        self.perfumes.loc[self.include, ['rel_q']] += self.question + " €{:0.2f}".format(value) + "\n"

        # self.perfumes.drop(index=indices, inplace=True)

    def reset_budget(self):
            self.perfumes.loc[self.exclude, ['included']] = True
            print("print rel_q",self.perfumes.loc[self.include, ['rel_q']])

            # Remove previous budget as reason
            #self.perfumes.loc[self.include, ['rel_q']].replace(to_replace=self.value, value="")

            self.value = None
            self.exclude = None
            self.include = None
            self.reason = None