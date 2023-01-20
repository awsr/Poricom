"""
Simple little scratchpad
"""

from PyQt5.QtWidgets import (QTextEdit)


class Scratchpad(QTextEdit):
    def __init__(self, parent=None, tracker=None):
        super(QTextEdit, self).__init__()
        self.parent = parent
        self.tracker = tracker
        self.setAcceptRichText(False)
        self.setObjectName("scratchpad")
        tracker.scratchpad = self