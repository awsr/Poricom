"""
Modify clipboard text for matched patterns
"""


class TextFormatter:
    def __init__(self):
        self._rules = None

    def set_rules(self, rules: list):
        self._rules = rules

    def process(self, text: str) -> str:
        for rule in self._rules:
            text = text.replace(rule[0], rule[1])

        return text


formatter = TextFormatter()
