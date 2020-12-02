import pandas as pd
from engine.question.QuestionType import QuestionType as qt
import xlrd
import openpyxl
from engine.question.QuestionChoice import QuestionChoice
import csv
from pathlib import Path


# The inference engine uses forward chaining and is based on a sort of fuzzy logic.
# Based on the answer to every questions, perfumes will be upvoted or downvoted.
class InferenceEngine:
    ## Attributes
    __questions = []
    __current_question = None
    __next_question_id = 2
    __final_question_id = 0
    __perfumes = []

    ## Constructor
    def __init__(self):
        # Set username: the name that we will use to address the user.
        self.username = "Sir/Madam"

        # Save all possible questions.
        self._read_questions()

        # Store all perfumes and their initial 'truth-values'.
        base_path = Path(__file__).parent
        # Set explicit path to filteredDatabase.csv
        database_path = (base_path / "../filteredDatabase.csv").resolve()
        self.__perfumes = pd.read_csv(open(database_path))
        truth_values = [0] * len(self.__perfumes.index)
        self.__perfumes['value'] = truth_values

    ## Methods

    # TODO for now, only reading multiple choice questions
    def _read_questions(self):
        base_path = Path(__file__).parent
        # Set explicit path to question_answer_pairs.csv
        questionanswer_path = (base_path / "../engine/question/data/question_answer_pairs.csv").resolve()
        questions = pd.read_csv(open(questionanswer_path))
        no_questions = len(questions.index)
        max_question_id = questions["ID"].iloc[no_questions - 1]
        self.__final_question_id = max_question_id
        self.__questions = self.__final_question_id * [None]

        for index in range(no_questions):
            line = questions.iloc[index]
            q = line["Question"]
            q_id = int(line["ID"])
            if line["Type"] == "Single":
                # Split answers if there are any
                if not pd.isna(line["Answers"]):
                    answers = line["Answers"].split(';')

                value = line["Value"]
                if isinstance(value, str):
                    value = value.split(';')

                next_ids = line["IDnext"]
                if isinstance(next_ids, str):
                    next_ids = next_ids.split(';')
                    next_ids = [int(i) for i in next_ids]

                self.__questions[q_id] = QuestionChoice(q_id,
                                                        q,
                                                        qt.CHOICE_SINGLE_SELECT,
                                                        self,
                                                        next_ids,
                                                        value,
                                                        answers)
            elif line["Type"] == "Drag":
                pass
            elif line["Type"] == "Text":
                pass

            if q_id > self.__final_question_id:
                self.__final_question_id = q_id

    # Check if we need to/can ask another question.
    def has_reached_goal(self):
        if self.__next_question_id == -1 or self.__next_question_id > self.__final_question_id \
                or not self.__next_question_id:
            return True
        return False
        # TODO Maybe we should add an option st the user is able to stop earlier?

    ## Getters and setters

    def set_username(self, name):
        self.username = name

    # Returns the next question and removes it from the list of remaining questions.
    def get_next_question(self):
        if not self.has_reached_goal():
            self.__current_question = self.__questions[self.__next_question_id]
            if (self.__current_question == None):
                print("NOTE: question with ID ", self.__next_question_id, " does not exist (yet).")
                exit(1)
            print(self.__current_question.question)
            self.__next_question_id = None
            return self.__current_question
        return None

    def set_answer(self, value):
        q = self.__current_question
        q.set_answer(value)

        if len(q.id_next) == 1:
            self.__next_question_id = q.id_next[0]
        elif not isinstance(value, int):
            index = q.answers.index(value)
            self.__next_question_id = index
        elif value >= len(q.id_next):
            print("Question ", q.id, " should have the same number of next IDs as answers (or only 1 next ID).")
            exit(1)
        else:
            self.__next_question_id = q.id_next[value]

        print("\nNext up: ", self.__next_question_id)

    # Returns a number of recommended perfumes based on the current state of the knowledge base.
    def get_recommendation(self):
        return self.__perfumes  # TODO for now


if __name__ == "__main__":
    engine = InferenceEngine()
    engine.set_username("Lonneke")
    while True:
        q = engine.get_next_question()
        print("Q: ", q.question)
        print("A: ", q.answers[0])
        engine.set_answer(0)
