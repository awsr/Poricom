"""
Simple little scratchpad
"""

from PyQt5.QtWidgets import (QTextEdit)


class Scratchpad(QTextEdit):
    def __init__(self):
        super(QTextEdit, self).__init__()
        self.setAcceptRichText(False)
        self.setObjectName("scratchpad")
