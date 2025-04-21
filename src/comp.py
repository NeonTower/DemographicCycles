from PySide6.QtWidgets import *

from src.autogen.ru_comp import Ui_ru_comp
from src.autogen.en_comp import Ui_en_comp


# Описание компьютерной модели на русском языке
class ru_comp(QDialog, Ui_ru_comp):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


# Описание компьютерной модели на английском языке
class en_comp(QDialog, Ui_en_comp):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
