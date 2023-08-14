"""
Poricom Popup Components

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QWidget, QLabel,
                             QLineEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox, QListWidget, QPushButton)
from PyQt5.QtGui import (QIcon)

from utils.config import (editSelectionConfig, editStylesheet)


class MessagePopup(QMessageBox):
    def __init__(self, title, message, flags=QMessageBox.Ok):
        super(QMessageBox, self).__init__(
            QMessageBox.NoIcon, title, message, flags)


class RuleLineEdit(QLineEdit):
    """Workaround QLineEdit class for an unusual bug causing the
       default button to lose its Default status the first time it
       gets and then loses focus. When this control gets focus,
       it will reset the targeted button's status as Default."""
    def __init__(self, parent):
        super().__init__(parent)
        self.default_target = None

    def focusInEvent(self, event):
        if self.default_target is not None:
            self.default_target.setDefault(True)
        super().focusInEvent(event)


class RulesPicker(QWidget):
    def __init__(self, parent, tracker):
        super(QWidget, self).__init__()
        self.setObjectName("rulespicker")
        self.parent = parent
        self.tracker = tracker
        self.raw_data = []
        # I know it's not the "proper" way of handling data in Qt, but it's good enough.

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(9, 9, 9, 9)

        self.input1 = RuleLineEdit(self)
        self.input2 = RuleLineEdit(self)
        self.button_add = QPushButton(QIcon(self.parent.config["RULES_PICKER_ICONS"]["add"]), "", self)
        self.button_add.setObjectName("rulespicker_btn_add")
        self.button_add.setDefault(True)
        self.button_del = QPushButton(QIcon(self.parent.config["RULES_PICKER_ICONS"]["del"]), "", self)
        self.button_del.setObjectName("rulespicker_btn_del")
        self.button_del.setAutoDefault(False)
        self.display_list = QListWidget(self)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName("rulesvertical")

        self.button_move_up = QPushButton(QIcon(self.parent.config["RULES_PICKER_ICONS"]["moveUp"]), "", self)
        self.button_move_up.setAutoDefault(False)
        self.button_move_up.setObjectName("rulespicker_btn_move_up")
        self.button_move_down = QPushButton(QIcon(self.parent.config["RULES_PICKER_ICONS"]["moveDown"]), "", self)
        self.button_move_down.setAutoDefault(False)
        self.button_move_down.setObjectName("rulespicker_btn_move_down")

        self.layout.addWidget(self.input1, 0, 0, 1, 1)
        self.layout.addWidget(self.input2, 0, 1, 1, 1)
        self.layout.addWidget(self.button_add, 0, 2, 1, 1)
        self.layout.addWidget(self.display_list, 1, 0, 1, 2)

        self.layout.addLayout(self.vertical_layout, 1, 2, 1, 1)
        self.vertical_layout.addWidget(self.button_del)
        self.vertical_layout.addStretch(1)
        self.vertical_layout.addWidget(self.button_move_up)
        self.vertical_layout.addWidget(self.button_move_down)
        self.vertical_layout.addStretch(1)

        self.input1.default_target = self.button_add
        self.input2.default_target = self.button_add

        self.button_add.clicked.connect(self.add_rule)
        self.button_del.clicked.connect(self.del_rule)
        self.button_move_up.clicked.connect(lambda: self.move_rule(True))
        self.button_move_down.clicked.connect(lambda: self.move_rule(False))
        self.display_list.currentRowChanged.connect(self.move_manager)

        if self.display_list.count() <= 1:
            self.button_move_up.setEnabled(False)
            self.button_move_down.setEnabled(False)

    def move_manager(self):
        """Enable/Disable move buttons depending on selection"""
        current_row = self.display_list.currentRow()
        if current_row == 0:
            self.button_move_up.setEnabled(False)
        else:
            self.button_move_up.setEnabled(True)

        if current_row == self.display_list.count() - 1:
            self.button_move_down.setEnabled(False)
        else:
            self.button_move_down.setEnabled(True)

    def add_rule(self):
        """Add input to internal rules list, add to list, and then clear inputs"""
        self.input1.setText(self.input1.text().strip())
        self.input2.setText(self.input2.text().strip())
        if self.input1.text() != "" and self.input2.text() != "":
            self.raw_data.append([self.input1.text(), self.input2.text()])
            self.display_list.addItem(self.format_to_text(self.input1.text(), self.input2.text()))
            self.input1.clear()
            self.input2.clear()
            self.input1.setFocus()

    def del_rule(self):
        """Delete rule at currently selected index (not entirely sure this is the right way)"""
        current_row = self.display_list.currentRow()
        if current_row >= 0:
            current_item = self.display_list.takeItem(current_row)
            del current_item
            current_rule = self.raw_data.pop(current_row)
            del current_rule

    def move_rule(self, up=False):
        """Move selected rule up or down"""
        current_row = self.display_list.currentRow()
        if current_row >= 0:
            current_item = self.display_list.takeItem(current_row)
            if up:
                self.display_list.insertItem(current_row - 1, current_item)
                self.display_list.setCurrentRow(current_row - 1)
            else:
                self.display_list.insertItem(current_row + 1, current_item)
                self.display_list.setCurrentRow(current_row + 1)

    def format_to_text(self, rule1, rule2=None):
        """String formatting"""
        if isinstance(rule1, list):
            return f"{rule1[0]} ⟹ {rule1[1]}"
        return f"{rule1} ⟹ {rule2}"

    def save_rules(self):
        """Save rules back out to config"""
        self.tracker.text_rules = self.raw_data


class TextModsPicker(RulesPicker):
    def __init__(self, parent, tracker):
        super().__init__(parent, tracker)

        for entry in self.tracker.text_rules:
            self.raw_data.append(entry)
            self.display_list.addItem(self.format_to_text(entry))

    def applyChanges(self):
        self.save_rules()
        return True


class BasePicker(QWidget):
    def __init__(self, parent, tracker, optionLists=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker
        if optionLists is None:
            optionLists = []

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        _comboBoxList = []
        _labelList = []

        for i, option in enumerate(optionLists):
            _comboBoxList.append(QComboBox())
            _comboBoxList[i].addItems(option)
            self.layout.addWidget(_comboBoxList[i], i, 1)
            _labelList.append(QLabel(""))
            self.layout.addWidget(_labelList[i], i, 0)

        self.pickTop = _comboBoxList[0]
        self.pickBot = _comboBoxList[-1]
        self.nameTop = _labelList[0]
        self.nameBot = _labelList[-1]

    def applySelections(self, selections):
        for selection in selections:
            index = getattr(self, f"{selection}Index")
            self.parent.config["SELECTED_INDEX"][selection] = index
            editSelectionConfig(index, selection)


class LanguagePicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["LANGUAGE"]
        listBot = config["ORIENTATION"]
        optionLists = [listTop, listBot]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeLanguage)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["language"])
        self.nameTop.setText("Language: ")
        self.pickBot.currentIndexChanged.connect(self.changeOrientation)
        self.pickBot.setCurrentIndex(config["SELECTED_INDEX"]["orientation"])
        self.nameBot.setText("Orientation: ")

        self.languageIndex = self.pickTop.currentIndex()
        self.orientationIndex = self.pickBot.currentIndex()

    def changeLanguage(self, i):
        self.languageIndex = i
        selectedLanguage = self.pickTop.currentText().strip()
        if selectedLanguage == "Japanese":
            self.tracker.language = "jpn"
        if selectedLanguage == "Korean":
            self.tracker.language = "kor"
        if selectedLanguage == "Chinese SIM":
            self.tracker.language = "chi_sim"
        if selectedLanguage == "Chinese TRA":
            self.tracker.language = "chi_tra"
        if selectedLanguage == "English":
            self.tracker.language = "eng"

    def changeOrientation(self, i):
        self.orientationIndex = i
        selectedOrientation = self.pickBot.currentText().strip()
        if selectedOrientation == "Vertical":
            self.tracker.orientation = "_vert"
        if selectedOrientation == "Horizontal":
            self.tracker.orientation = ""

    def applyChanges(self):
        self.applySelections(['language', 'orientation'])
        return True


class FontPicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["FONT_STYLE"]
        listBot = config["FONT_SIZE"]
        optionLists = [listTop, listBot]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeFontStyle)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["fontStyle"])
        self.nameTop.setText("Font Style: ")
        self.pickBot.currentIndexChanged.connect(self.changeFontSize)
        self.pickBot.setCurrentIndex(config["SELECTED_INDEX"]["fontSize"])
        self.nameBot.setText("Font Size: ")

        self.fontStyleText = "  font-family: 'Poppins';\n"
        self.fontSizeText = "  font-size: 16pt;\n"
        self.fontStyleIndex = self.pickTop.currentIndex()
        self.fontSizeIndex = self.pickBot.currentIndex()

    def changeFontStyle(self, i):
        self.fontStyleIndex = i
        selectedFontStyle = self.pickTop.currentText().strip()
        replacementText = f"  font-family: '{selectedFontStyle}';\n"
        self.fontStyleText = replacementText

    def changeFontSize(self, i):
        self.fontSizeIndex = i
        selectedFontSize = int(self.pickBot.currentText().strip())
        replacementText = f"  font-size: {selectedFontSize}pt;\n"
        self.fontSizeText = replacementText

    def applyChanges(self):
        self.applySelections(['fontStyle', 'fontSize'])
        editStylesheet(41, self.fontStyleText)
        editStylesheet(42, self.fontSizeText)
        return True


class ScaleImagePicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["IMAGE_SCALING"]
        optionLists = [listTop]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeScaling)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["imageScaling"])
        self.nameTop.setText("Image Scaling: ")

        self.imageScalingIndex = self.pickTop.currentIndex()

    def changeScaling(self, i):
        self.imageScalingIndex = i

    def applyChanges(self):
        self.applySelections(['imageScaling'])
        self.parent.canvas.setViewImageMode(self.imageScalingIndex)
        return True


class ShortcutPicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["MODIFIER"]
        optionLists = [listTop]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeModifier)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["modifier"])
        self.nameTop.setText("Modifier: ")

        self.pickBot = QLineEdit(config["SHORTCUT"]["captureExternalKey"])
        self.layout.addWidget(self.pickBot, 1, 1)
        self.nameBot = QLabel("Key: ")
        self.layout.addWidget(self.nameBot, 1, 0)

        self.modifierIndex = self.pickTop.currentIndex()

    def keyInvalidError(self):
        MessagePopup(
            "Invalid Key",
            "Please select an alphanumeric key."
        ).exec()

    def changeModifier(self, i):
        self.modifierIndex = i

    def setShortcut(self, keyName, modifierText, keyText):

        tooltip = f"{self.parent.config['SHORTCUT'][f'{keyName}Tip']}{modifierText}{keyText}."
        self.parent.config["SHORTCUT"][keyName] = f"{modifierText}{keyText}"
        self.parent.config["SHORTCUT"][f"{keyName}Key"] = keyText
        self.parent.config["TBAR_FUNCS"]["FILE"][f"{keyName}Helper"]["helpMsg"] = tooltip

    def applyChanges(self):
        selectedModifier = self.pickTop.currentText().strip() + "+"
        if selectedModifier == "No Modifier+":
            selectedModifier = ""

        if not self.pickBot.text().isalnum():
            self.keyInvalidError()
            return False
        if len(self.pickBot.text()) != 1:
            self.keyInvalidError()
            return False

        self.setShortcut('captureExternal', selectedModifier,
                         self.pickBot.text())
        self.applySelections(['modifier'])
        return True


class PickerPopup(QDialog):
    def __init__(self, widget):
        super(QDialog, self).__init__(None,
                                      Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.widget = widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(widget)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout().addWidget(self.buttonBox)

        # Stop annoying autoDefault behavior stealing from explicit defaults
        for button in self.buttonBox.buttons():
            button.setAutoDefault(False)

        self.buttonBox.rejected.connect(self.cancelClickedEvent)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        if self.widget.applyChanges():
            return super().accept()

    def cancelClickedEvent(self):
        self.close()
