
# A general question. Meant as an abstract class! (But unfortunately, you can't make a class abstract
# explicitly in Python.)
class Question:
    def __init__(self, q_id, question, q_type, engine, id_next, value):
        self.id = q_id
        self.engine = engine
        self.type = q_type
        self.question = question
        self.id_next = id_next
        self.value = value

    def set_answer(self, value):
        pass
