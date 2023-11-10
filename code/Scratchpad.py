"""
Simple little scratchpad
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTextEdit, QShortcut, QApplication
from PyQt5.QtGui import QContextMenuEvent


class Scratchpad(QTextEdit):
    def __init__(self, parent=None, tracker=None):
        super().__init__()
        self.parent = parent
        self.tracker = tracker
        self.setAcceptRichText(False)
        self.setObjectName("scratchpad")
        tracker.scratchpad = self

        self._move_op = self.textCursor().MoveOperation.End

        self.shortcut_append = QShortcut("Ctrl+Shift+V", self)
        self.shortcut_append.activated.connect(self.append_paste)

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        menu = self.createStandardContextMenu()
        append_action = menu.addAction("Append", self.append_paste, "Ctrl+Shift+V")
        append_separator = menu.addSeparator()
        menu.insertAction(menu.actions()[0], append_separator)
        menu.insertAction(append_separator, append_action)
        menu.exec(e.globalPos())

    @pyqtSlot()
    def append_paste(self):
        clipboard_text = QApplication.clipboard().text()
        if len(clipboard_text) > 0:
            self.append(clipboard_text)
            self.moveCursor(self._move_op)
