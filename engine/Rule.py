
# A simple rule of the form
#   A and B and ... and W --> X and ... and Z
class Rule:
    premise = []  # type: [Fact]
    conclusion = []  # type: [Fact]

    def __init__(self, ifs, then):
        self.premise = ifs
        self.conclusion = then

    def infer(self, facts):
        for f in facts:
            if f not in self.premise:
                return
        # TODO set facts to their corresponding truth-value

