from pathlib import Path
import pandas as pd
from engine.question.Question import Question
from engine.question.QuestionType import QuestionType as qt


class QuestionDropdown(Question):
    def __init__(self, q_id, question, engine, id_next, labels, value, perfumes):
        super().__init__(q_id,
                         question,
                         qt.DROPDOWN,
                         engine,
                         id_next,
                         labels,
                         value,
                         perfumes)

    def get_perfumes(self):
        products = len(self.perfumes.index) * [""]
        df = self.perfumes[["Title", "Vendor"]]

        for index, item in df.iterrows():
            name = item["Title"] + " (" + item["Vendor"] + ")"
            products[index] = name

        return products,None

    def get_families(self):
        base_path = Path(__file__).parent
        families_path = (base_path / "../question/data/olfactory_families.csv").resolve()
        families = pd.read_csv(open(families_path), encoding="utf-8")
        return families["Family"].tolist(),families["Tag"].tolist()

    def get_ingredients(self):
        base_path = Path(__file__).parent
        ingredients_path = (base_path / "../question/data/ingredients.csv").resolve()
        ingredients = pd.read_csv(open(ingredients_path), encoding="utf-8")
        return ingredients["Ingredient"].tolist(),ingredients["Tag"].tolist()

    def set_answer(self, perfume_indices):
        print("Setting answer QuestionDropdown: ", perfume_indices)
        print(type(self.perfumes.loc[perfume_indices, ["rank"]]))
        print(self.perfumes.loc[perfume_indices, ["rank"]])
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
