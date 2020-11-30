from engine.Fact import FactType, Fact
import pandas as pd
from constants import *
import xlrd
import openpyxl


# TODO Python notes to self:
# - if the constructor does 'self.x = ...', x doesn't need to be explicitly defined as an attribute.
# - private attribute x: __x
# - (sort of) protected attribute x: _x
# - public attribute x: x


# The inference engine uses forward chaining and is based on a sort of fuzzy logic.
# Based on the answer to every questions, perfumes will be upvoted or downvoted.
from engine.question.Question import Question
from engine.question.QuestionMultipleChoice import QuestionMultipleChoice


class InferenceEngine:
    # Attributes
    __questions = []
    # __facts = []
    __perfumes = []

    # Constructor
    # username: string
    # perfumes: pandas dataframe
    def __init__(self, username, perfumes):
        # Set username: the name that we will use to address the user.
        self.username = username

        # Save all possible facts and initialise their truth-values to None (unknown).
        # self.__facts = [Fact(t) for t in list(FactType)]

        # Save all possible questions.
        self._read_questions()

        # Store all perfumes and their initial 'truth-values'.
        self.__perfumes = perfumes
        truth_values = [0.5] * len(perfumes.index)
        self.__perfumes['value'] = truth_values

    # TODO for now, only reading multiple choice questions
    def _read_questions(self):
        questions = pd.read_csv(questions_file)
        no_questions = len(questions.index)
        self.__questions = no_questions * [0]
        for index in range(no_questions):
            q = questions.iloc[index][0]
            answers = [questions.iloc[index][a] for a in range(1, len(questions.columns)) if a != ""]
            self.__questions[index] = QuestionMultipleChoice(q, answers)

    def run(self):
        while not self.has_reached_goal():
            self.get_next_question()
            # FIXME somehow wait for answer and receive it...

        return self.get_recommendation()

    # Check if we need to/can ask another question.
    def has_reached_goal(self):
        return self.__questions == []
        # TODO. For now, check if there are no questions left to answer.
        # Maybe we should add an option st the user is able to stop earlier?

    # Returns the next question and removes it from the list of remaining questions.
    def get_next_question(self):
        assert self.__questions != []
        return self.__questions.pop(0)  # TODO for now, simply ask the following question

    # Returns a number of recommended perfumes based on the current state of the knowledge base.
    def get_recommendation(self):
        return self.__perfumes  # TODO for now


if __name__ == "__main__":
    perfumes = pd.read_csv(filtered_database_file)
    engine = InferenceEngine("Lonneke", perfumes)
