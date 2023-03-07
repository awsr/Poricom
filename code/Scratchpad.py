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

        self.addTextSc = QShortcut("Ctrl+Shift+V", self)
        self.addTextSc.activated.connect(lambda: self.append(QApplication.clipboard().text()))

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        self.menu = self.createStandardContextMenu()
        self.appendAction = self.menu.addAction("Append", lambda: self.append(QApplication.clipboard().text()), "Ctrl+Shift+V")
        self.appendSeparator = self.menu.addSeparator()
        self.menu.insertAction(self.menu.actions()[0], self.appendSeparator)
        self.menu.insertAction(self.appendSeparator, self.appendAction)
        self.menu.exec(e.globalPos())