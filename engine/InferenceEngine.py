import pandas as pd

from engine.question.QuestionDropdown import QuestionDropdown
from engine.question.QuestionChoiceMultiple import QuestionChoiceMultiple
from engine.question.QuestionChoiceSingle import QuestionChoiceSingle
from engine.question.QuestionDisplay import QuestionDisplay
from pathlib import Path
import math

from engine.question.QuestionBudget import QuestionBudget
from engine.question.QuestionName import QuestionName
from engine.question.QuestionType import QuestionType as qt


# The inference engine uses forward chaining and is based on a sort of fuzzy logic.
# Based on the answer to every questions, perfumes will be upvoted or downvoted.
class InferenceEngine:
    ## Attributes
    __questions = []
    __current_question = None
    __previous_question = None
    __traversed_path = []
    __previous_question_id = 0
    __next_question_id = 1
    __final_question_id = 0
    __question_direction = 1
    __perfumes = []
    __additional_info = {}

    ## Constructor
    def __init__(self):
        # 1. Store all perfumes and their initial 'truth-values'.

        # 1a. Set explicit path to filteredDatabase.csv
        base_path = Path(__file__).parent
        database_path = (base_path / "../data/filteredDatabase.csv").resolve()
        self.__perfumes = pd.read_csv(open(database_path, encoding="utf-8"))

        # 1b. Add the two ways based on which we recommend perfumes, ranks and inclusion/exclusion.
        #  - Add truth-values, also known as ranks.
        truth_values = [0.0] * len(self.__perfumes.index)
        self.__perfumes['rank'] = truth_values

        #  - Add column with booleans, representing if the perfume can be included in the recommendations.
        included = [True] * len(self.__perfumes.index)
        self.__perfumes['included'] = included

        # 1c. Add column where we can explain _why_ it has a certain truth value.
        facts = [''] * len(self.__perfumes.index)
        self.__perfumes['facts'] = facts

        # 2. Save all possible questions.
        self._read_questions()

    #############
    ## Methods ##

    def reset(self):
        # Store all perfumes and their initial 'truth-values'.
        # base_path = Path(__file__).parent

        # Set explicit path to filteredDatabase.csv
        # database_path = (base_path / "../filteredDatabase.csv").resolve()

        # self.__perfumes = pd.read_csv(open(database_path, encoding="utf-8"))

        # Reset ranks
        truth_values = [0.0] * len(self.__perfumes.index)
        self.__perfumes['rank'] = truth_values

        # Include all perfumes
        included = [True] * len(self.__perfumes.index)
        self.__perfumes['included'] = included

        # Reset facts, the reasons for recommendations
        facts = [''] * len(self.__perfumes.index)
        self.__perfumes['facts'] = facts

        # No need to reset __final_question_id or __questions
        self.__current_question = None
        self.__next_question_id = 2  # Skip the name question, with question ID 1.
        self.__additional_info = {}


    def _read_questions(self):
        base_path = Path(__file__).parent
        # Set explicit path to question_answer_pairs.csv
        questionanswer_path = (base_path / "../data/question_answer_pairs.csv").resolve()
        questions = pd.read_csv(open(questionanswer_path), encoding="utf-8")
        no_questions = len(questions.index)
        max_question_id = questions["ID"].iloc[no_questions - 1]
        self.__final_question_id = max_question_id
        self.__questions = (self.__final_question_id + 1) * [None]  # + 1 door zero-indexing, maar IDs beginnen bij 1

        for index in range(no_questions):
            line = questions.iloc[index]
            q = line["Question"]
            q_id = int(line["ID"])

            if line["Type"] == "Single" \
                    or line["Type"] == "Multiple" \
                    or line["Type"] == "Drag" \
                    or line["Type"] == "Text" \
                    or line["Type"] == "Number":
                # Split answers if there are any
                answers = None
                if not pd.isna(line["Answers"]):
                    answers = line["Answers"].split(';')

                next_ids = line["IDnext"]
                if isinstance(next_ids, str):
                    next_ids = next_ids.split(';')
                    next_ids = [int(i) if i != 'END' else -1 for i in next_ids]

                labels = line["Labels"]
                if isinstance(labels, str):
                    labels = labels.split(';')

                value = line["Value"]
                if isinstance(value, str):
                    value = value.split(';')
                    value = [float(x) for x in value if x != '']
                if line["Type"] == "Single":
                    self.__questions[q_id] = QuestionChoiceSingle(q_id=q_id,
                                                                  question=q,
                                                                  engine=self,
                                                                  id_next=next_ids,
                                                                  labels=labels,
                                                                  value=value,
                                                                  perfumes=self.__perfumes,
                                                                  answer_options=answers)
                elif line["Type"] == "Multiple":
                    self.__questions[q_id] = QuestionChoiceMultiple(q_id=q_id,
                                                                    question=q,
                                                                    engine=self,
                                                                    id_next=next_ids,
                                                                    labels=labels,
                                                                    value=value,
                                                                    perfumes=self.__perfumes,
                                                                    answer_options=answers)
                elif line["Type"] == "Drag":
                    self.__questions[q_id] = QuestionDropdown(q_id=q_id,
                                                              question=q,
                                                              engine=self,
                                                              id_next=next_ids,
                                                              labels=labels,
                                                              value=value,
                                                              perfumes=self.__perfumes)
                elif line["Type"] == "Text":
                    self.__questions[q_id] = QuestionName(q_id=q_id,
                                                          question=q,
                                                          engine=self,
                                                          id_next=next_ids,
                                                          perfumes=self.__perfumes)
                elif line["Type"] == "Number":
                    self.__questions[q_id] = QuestionBudget(q_id=q_id,
                                                            question=q,
                                                            engine=self,
                                                            id_next=next_ids,
                                                            perfumes=self.__perfumes)
            elif line["Type"] == "Display":
                next_ids = line["IDnext"]
                if isinstance(next_ids, str):
                    next_ids = next_ids.split(';')
                    next_ids = [int(i) for i in next_ids]

                self.__questions[q_id] = QuestionDisplay(q_id,
                                                         q,
                                                         self,
                                                         next_ids,
                                                         labels,
                                                         value,
                                                         self.__perfumes,
                                                         answers)

            if q_id > self.__final_question_id:
                self.__final_question_id = q_id

    # Check if we need to/can ask another question.
    def has_reached_goal(self):
        if self.__next_question_id == -1 or self.__next_question_id > self.__final_question_id \
                or not self.__next_question_id:
            return True
        return False
        # TODO Maybe we should add an option st the user is able to stop earlier?

    def add_additional_info(self, entry_name, value):
        self.__additional_info[entry_name] = value

    #########################
    ## Getters and setters ##

   
    # Value 0 being backwards, 1 being forwards
    def set_question_direction(self, value):
        self.__question_direction = value

    def get_question_direction(self):
        return self.__question_direction

    def get_current_question(self):
        return self.__current_question

    def set_current_question(self, value):
        self.__current_question = value

    def get_next_question_id(self):
        return self.__next_question_id

    # Returns the most recent previous question the user answered.
    def get_previous_question(self):
        # The name question is the first, so we can't go back
        if not self.__previous_question_id == 0:
            # Get most recent answered question
            self.__previous_question = self.__questions[self.__traversed_path.pop()]
            if self.__previous_question is None:
                print("NOTE: previous question with ID ", self.__previous_question_id, " does not exist (yet).")
                exit(1)
        return self.__previous_question


    # Returns the next question from the list.
    def get_next_question(self):
        if not self.has_reached_goal():
            self.__current_question = self.__questions[self.__next_question_id]
            if self.__current_question is None:
                print("NOTE: question with ID ", self.__next_question_id, " does not exist (yet).")
                exit(1)
            print(self.__current_question.question)
            return self.__current_question
        return None

    def set_answer(self, value):
        # Set answer inside relevant question
        q = self.__current_question
        q.set_answer(value)
        self.__previous_question_id = q.id
        
        # Set next question id
        if len(q.id_next) == 1:  # Only one possible next question
            self.__next_question_id = q.id_next[0]
        elif q.type == qt.SINGLE:  # Only one possible answer, which is linked to a next question
            # value has type int
            self.__next_question_id = q.id_next[value]
        elif q.type == qt.MULTIPLE:  # Multiple answers could have been selected
            # value has type list
            ids = [q.id_next[index] for index, x in enumerate(value) if x == 1]
            if len(ids) != 0: 
                self.__next_question_id = min(ids)  # Selected the next question with the lowest id
            else: 
                ids = [q.id_next[index] for index, x in enumerate(value) if x == 0]
                self.__next_question_id = max(ids)  # no answer was selected, skip extra questions
        else:
            print("Multiple possible next questions for unhandled question type: ", q.type)
            exit(1)
            
        # Add questionID that was just answered to the path of questions
        self.__traversed_path.append(q.id)
        print(self.__traversed_path)
        print("\nNext up: ", self.__next_question_id)

    # Returns a number of recommended perfumes based on the current state of the knowledge base.
    def get_recommendations(self):
        possibilities = self.__perfumes[self.__perfumes['included'] == True]
        sorted_list = possibilities.sort_values(axis=0, by="rank", ascending=False, inplace=False)
        return sorted_list.iloc[0:5, :]

    # Returns the min and max price of the top 20 products that are left.
    def get_price_range(self):
        sorted_list = self.__perfumes.sort_values(axis=0, by="rank", ascending=False, inplace=False)
        top20 = sorted_list.iloc[0:20, :]
        maxPrice = math.ceil(float(top20['Price'].max()))
        minPrice = math.ceil(float(top20['Price'].min()))
        return minPrice, maxPrice


if __name__ == "__main__":
    engine = InferenceEngine()

    while True:
        q = engine.get_next_question()
        print("Q: ", q.question)
        print("A: ", q.answers[0])
        engine.set_answer(0)
