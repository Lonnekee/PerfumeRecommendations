from enum import Enum, unique, auto


@unique
class FactType(Enum):
    LIKE_ROSES = auto()


class Fact:
    value = None

    def __init__(self, fact_type):
        self.type = fact_type

