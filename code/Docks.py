from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDockWidget


class DockBase(QDockWidget):
    def __init__(self, parent=None, widget=None, allowFloat=False):
        super().__init__(parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        if (allowFloat):
            self.setFeatures(QDockWidget.DockWidgetFloatable)
        else:
            self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.container = QWidget()
        self.container.setMinimumSize(100, 100)
        self.vertLayout = QVBoxLayout(self.container)
        self.vertLayout.setContentsMargins(0, 0, 0, 0)
        self.vertLayout.addWidget(widget)
        self.setWidget(self.container)
