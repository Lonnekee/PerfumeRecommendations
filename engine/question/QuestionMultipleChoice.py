from engine.question.Question import Question


# TODO Single select multiple choice or multi select multiple choice.
class QuestionMultipleChoice(Question):
    def __init__(self, question, answer_options):
        super().__init__(question)
        self.answers = answer_options
