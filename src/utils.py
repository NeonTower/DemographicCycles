from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtWidgets import *
from PySide6.QtGui import QDoubleValidator, QIntValidator

# Делегат для корректного ввода времени t
class TimeDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QIntValidator(0, 4500)
        editor.setValidator(validator) 
        return editor

# Делегат для корректного ввода параметров r и q
class FloatDelegate(QStyledItemDelegate):
    def __init__(self, min_value=None, max_value=None, decimals=2, parent=None):
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value
        self.decimals = decimals

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator(self.min_value, self.max_value, self.decimals)
        editor.setValidator(validator) 
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

# Прокси-модель для правильной сортировки значений
class NumericSortProxyModel(QSortFilterProxyModel):
    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left, Qt.EditRole)
        right_data = self.sourceModel().data(right, Qt.EditRole)

        if left_data is None or right_data is None:
            return super().lessThan(left, right)

        try:
            left_value = float(left_data)
            right_value = float(right_data)
            return left_value < right_value
        except ValueError:
            return super().lessThan(left, right)