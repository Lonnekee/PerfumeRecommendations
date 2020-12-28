from engine.question.Question import Question


class QuestionChoice(Question):
    def __init__(self, q_id, question, q_type, engine, id_next, labels, value, perfumes, answer_options):
        super().__init__(q_id, question, q_type, engine, id_next, labels, value, perfumes)
        self.answers = answer_options

    def _update_ranks(self, labels, value, answer_index):
        data = self.perfumes
        labels = labels.split('+')

        for lab in labels:
            if lab == '':
                continue

            # Get the relevant column to search for label
            column = None
            if lab.startswith('Collection:'):
                column = 'Collection'
            elif lab.startswith('Tag:'):
                column = 'Tag'
            elif lab.startswith('Vendor:'):
                column = 'Vendor'
            elif lab.startswith('Type:'):
                column = 'Type'
            else:
                print('  QuestionChoice: column type not recognized! (Only Tag, Vendor are known.)')
                continue

            lab = lab[len(column) + 1:]

            # Select all perfumes that contain the relevant label
            print("  Searching for ", lab, " in ", column)
            rows = data[column].str.contains(lab)
            print("  Found: ", rows.sum())

            # Add the value specified for this label
            data.loc[rows, ['rank']] += float(value)
            print("  Updated with: ", float(value))

            # Store the reason why we updated these perfumes
            data.loc[rows, ['facts']] += self.answers[answer_index]
