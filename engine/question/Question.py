# A general question. Meant as an abstract class! (But unfortunately, you can't make a class abstract
# explicitly in Python.)
class Question:
    answers = []

    def __init__(self, question): # , related_fact
        self.question = question
        # self.related_fact = related_fact

    def set_answer(self, value):
        # self.related_fact.value = value
        pass
