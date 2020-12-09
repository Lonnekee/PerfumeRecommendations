from pathlib import Path
import pandas as pd
from engine.question.Question import Question
from engine.question.QuestionType import QuestionType as qt


class QuestionDropdown(Question):
    def __init__(self, q_id, question, engine, id_next, labels, value, perfumes):
        super().__init__(q_id,
                         question,
                         qt.CHOICE_DROPDOWN,
                         engine,
                         id_next,
                         labels,
                         value,
                         perfumes)

    def set_answer(self, perfume_indices):
        print("Setting answer QuestionDropdown: ", perfume_indices)

        self.perfumes.loc[perfume_indices, ["rank"]] += self.value


if __name__ == "__main__":
    # Store all perfumes and their initial 'truth-values'.
    base_path = Path(__file__).parent
    # print(base_path)
    # Set explicit path to filteredDatabase.csv
    database_path = (base_path / "../../filteredDatabase.csv").resolve()
    # print(database_path)
    perfumes = pd.read_csv(open(database_path, encoding="utf-8"))
    truth_values = [0] * len(perfumes.index)
    perfumes['rank'] = truth_values

    q = QuestionDropdown(1, "hello?", None, None, ["doesn't matter"], 1.0, perfumes)
    q.set_answer([2, 4])
