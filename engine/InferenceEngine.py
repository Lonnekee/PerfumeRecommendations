import pandas as pd
from constants import *
from engine.question.QuestionType import QuestionType as qt
import xlrd
import openpyxl
from engine.question.QuestionChoice import QuestionChoice


# The inference engine uses forward chaining and is based on a sort of fuzzy logic.
# Based on the answer to every questions, perfumes will be upvoted or downvoted.
class InferenceEngine:
    ## Attributes
    __questions = []
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
        self.__perfumes = pd.read_csv(filtered_database_file)
        truth_values = [0] * len(self.__perfumes.index)
        self.__perfumes['value'] = truth_values

    ## Methods

    # TODO for now, only reading multiple choice questions
    def _read_questions(self):
        questions = pd.read_csv(questions_file)
        no_questions = len(questions.index)
        max_question_id = questions["ID"].iloc[no_questions-1]
        self.__final_question_id = max_question_id
        self.__questions = self.__final_question_id * [None]

        for index in range(no_questions):
            line = questions.iloc[index]
            q = line["Question"]
            q_id = int(line["ID"])
            if line["Type"] == "Single":
                answers = line["Answers"].split(';')

                value = line["Value"]
                if isinstance(line["Value"], str):
                    value.split(';')

                self.__questions[q_id] = QuestionChoice(q_id,
                                                         q,
                                                         qt.CHOICE_SINGLE_SELECT,
                                                         self,
                                                         line["IDnext"].split(';'),
                                                         value,
                                                         answers)
            elif line["Type"] == "Drag":
                pass
            elif line["Type"] == "Text":
                pass

            if q_id > self.__final_question_id:
                self.__final_question_id = q_id

    # Check if we need to/can ask another question.
    def _has_reached_goal(self):
        if self.__next_question_id == -1 or self.__next_question_id > self.__final_question_id\
                or not self.__next_question_id:
            return True
        return False
        # TODO Maybe we should add an option st the user is able to stop earlier?


    ## Getters and setters

    def set_username(self, name):
        self.username = name

    # Returns the next question and removes it from the list of remaining questions.
    def get_next_question(self):
        if not self._has_reached_goal():
            return self.__questions[self.__next_question_id]
        return None

    def set_next_question(self, value):
        print("Set next question: ", value)
        self.__next_question_id = int(value)

    # Returns a number of recommended perfumes based on the current state of the knowledge base.
    def get_recommendation(self):
        return self.__perfumes  # TODO for now


if __name__ == "__main__":
    engine = InferenceEngine()
    engine.set_username("Lonneke")
    while True:
        q = engine.get_next_question()
        print(q)
        print(q.question)
        print("Answer: ", q.answers[0])
        q.set_answer(0)
