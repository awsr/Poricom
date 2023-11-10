"""
Data models for Qt views
"""

from PyQt5.QtCore import Qt, QAbstractListModel


class RuleModel(QAbstractListModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

    def rowCount(self, index):
        return len(self.rules)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            rule_from, rule_to = self.rules[index.row()]
            return f"{rule_from} ⟹ {rule_to}"
