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
        self.tags = None
        self.vendor = None

    def get_list(self):
        if "takePerfume" in self.labels:
            return self.__get_perfumes()  # lists of strings, describing perfume name and brand and their tags
        elif "takeFamily" in self.labels:
            return self.__get_families()  # lists of strings, describing olfactory families and their tags
        elif "takeIngredient" in self.labels:
            return self.__get_ingredients()  # lists of strings, describing ingredients and their tags
        else:
            print("Appropriate dropdown not found.")
            return None

    def __get_perfumes(self):
        base_path = Path(__file__).parent
        perfumes_path = (base_path / "../../data/filteredDatabase.csv").resolve()
        perfumes = pd.read_csv(open(perfumes_path), encoding="utf-8")

        df = perfumes[["Title", "Vendor"]]
        products = len(df.index) * [""]
        for index, item in df.iterrows():
            name = item["Title"] + " (" + item["Vendor"] + ")"
            products[index] = name

        # find the related families to the perfumes
        families = []
        for index, item in perfumes["Tag"].items():
            sp = item.split()
            string = ""
            for w in sp:
                if w.startswith("Familie:"):
                    string = string + w + "+"
            families.append(string[:-1].replace(",",""))
        
        self.tags = families
        self.vendor = perfumes["Vendor"].tolist()
        return products  # send all products in a list

    def __get_families(self):
        base_path = Path(__file__).parent
        families_path = (base_path / "../../data/olfactory_families.csv").resolve()
        families = pd.read_csv(open(families_path), encoding="utf-8")
        self.tags = families["Tag"].tolist() 
        return families["Family"].tolist()  # send all families in a list

    def __get_ingredients(self):
        base_path = Path(__file__).parent
        ingredients_path = (base_path / "../../data/ingredients.csv").resolve()
        ingredients = pd.read_csv(open(ingredients_path), encoding="utf-8")
        self.tags = ingredients["Tag"].tolist()
        return ingredients["Ingredient"].tolist()  # send all ingredients  in a list

    def set_answer(self, indices):
        print("Setting answer QuestionDropdown: ", indices)

        # For all indices, upvote products with specific tag
        if self.tags is not None:
            for index in indices:
                labels = self.tags[index].split('+')
                for lab in labels:
                    if lab == '':
                        continue

                    # Select all perfumes that contain the relevant label
                    print("  Searching for ", lab, " in Tag")
                    rows = self.perfumes['Tag'].str.contains(lab)
                    print("  Found: ", rows.sum())

                    # Add the value linked to this question
                    self.perfumes.loc[rows, ['rank']] += float(self.value[0])

                    # Add reason for upvoting/downvoting
                    self.perfumes.loc[rows, ['rel_q']] += self.question + " " + self.tags[index] + "\n"
                    self.perfumes.loc[rows, ['facts']] += self.tags[index] + ", "

        # For all indices, upvote products with specific vendor
        if self.vendor is not None:
            for index in indices:
                labels = self.vendor[index].split('+')
                for lab in labels:
                    if lab == '':
                        continue

                    # Select all perfumes that contain the relevant label
                    print("  Searching for ", lab, " in Vendor")
                    rows = self.perfumes['Vendor'].str.contains(lab)
                    print("  Found: ", rows.sum())

                    # Add the value specified for this label
                    self.perfumes.loc[rows, ['rank']] += float(self.value[0])
                    print("  Updated with: ", float(self.value[0]))

                    # Add reason for upvoting/downvoting
                    self.perfumes.loc[rows, ['facts']] += self.vendor[index] + " "

        # if the question is about the perfumes, make sure the selected products (either liked or disliked) get
        # downvoted a lot these are either already known or disliked
        if "takePerfume" in self.labels:
            print("Downvote selected perfumes")
            self.perfumes.loc[indices, ['rank']] += -100


if __name__ == "__main__":
    # Store all perfumes and their initial 'truth-values'.
    base_path = Path(__file__).parent
    # print(base_path)
    # Set explicit path to filteredDatabase.csv
    database_path = (base_path / "../../data/filteredDatabase.csv").resolve()
    # print(database_path)
    perfumes = pd.read_csv(open(database_path, encoding="utf-8"))
    truth_values = [0] * len(perfumes.index)
    perfumes['rank'] = truth_values

    q = QuestionDropdown(1, "hello?", None, None, ["doesn't matter"], 1.0, perfumes)
    q.set_answer([2, 4])
