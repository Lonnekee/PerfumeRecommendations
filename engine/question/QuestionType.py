from enum import Enum, unique, auto


@unique
class QuestionType(Enum):
    CHOICE_SINGLE_SELECT = auto(),
    CHOICE_MULTIPLE_SELECT = auto(),
    CHOICE_DISPLAY = auto(),
    INTEGER = auto(),
    STRING = auto(),
    CHOICE_DROPDOWN = auto()
