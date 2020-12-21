from enum import Enum, unique, auto


@unique
class QuestionType(Enum):
    SINGLE = auto(),
    MULTIPLE = auto(),
    DISPLAY = auto(),
    BUDGET = auto(),
    NAME = auto(),
    DROPDOWN = auto()
