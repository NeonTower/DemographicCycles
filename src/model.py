from PySide6.QtWidgets import *

from src.autogen.ru_model import Ui_ru_model
from src.autogen.en_model import Ui_en_model


# Описание математической модели на русском языке
class ru_model(QDialog, Ui_ru_model):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


# Описание математической модели на английском языке
class en_model(QDialog, Ui_en_model):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
