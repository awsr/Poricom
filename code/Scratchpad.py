"""
Simple little scratchpad
"""

from PyQt5.QtWidgets import (QTextEdit, QShortcut, QApplication)
from PyQt5.QtGui import (QContextMenuEvent)


class Scratchpad(QTextEdit):
    def __init__(self, parent=None, tracker=None):
        super(QTextEdit, self).__init__()
        self.parent = parent
        self.tracker = tracker
        self.setAcceptRichText(False)
        self.setObjectName("scratchpad")
        tracker.scratchpad = self

        self.menu = self.createStandardContextMenu()
        self.append_action = self.menu.addAction("Append", lambda: self.append(QApplication.clipboard().text()), "Ctrl+Shift+V")
        self.append_separator = self.menu.addSeparator()
        self.menu.insertAction(self.menu.actions()[0], self.append_separator)
        self.menu.insertAction(self.append_separator, self.append_action)

        self.shortcut_append = QShortcut("Ctrl+Shift+V", self)
        self.shortcut_append.activated.connect(lambda: self.append(QApplication.clipboard().text()))

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        self.menu.exec(e.globalPos())
