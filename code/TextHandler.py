"""
Modify clipboard text for matched patterns
"""

class TextFormatter():
    def __init__(self):
        self._rules = None

    def set_rules(self, rules):
        self._rules = rules

    def process(self, text):
        for i, rule in enumerate(self._rules):
            text = text.replace(rule[0], rule[1])

        return text

formatter = TextFormatter()
