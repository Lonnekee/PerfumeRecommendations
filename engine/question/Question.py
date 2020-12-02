
# A general question. Meant as an abstract class! (But unfortunately, you can't make a class abstract
# explicitly in Python.)
class Question:
    def __init__(self, q_id, question, q_type, engine, id_next, labels, value, perfumes):
        self.id = q_id             # type: int
        self.engine = engine       # type: InferenceEngine
        self.type = q_type         # type: QuestionType
        self.question = question   # type: string
        self.id_next = id_next     # type: [ int ]
        self.labels = labels       # type: [ string ]
        self.value = value         # type: [ double ]
        self.perfumes = perfumes   # type: Pandas DataFrame

    def set_answer(self, value):
        print("Setting answer: ", value)
