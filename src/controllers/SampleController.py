from PySide6.QtCore import Slot, QObject
from PySide6.QtGui import QStandardItem

from src import MainUI


# Часть логики, отвечающая за установку предопределённых примеров
class SampleController(QObject):
    def __init__(self, main: MainUI):
        self.main = main

        self.main.sample1_action.triggered.connect(self.on_sample1)
        self.main.sample2_action.triggered.connect(self.on_sample2)
        self.main.sample3_action.triggered.connect(self.on_sample3)

    # Пример 1 -- константный метод
    @Slot()
    def on_sample1(self):
        self.main.ex1_frame.setHidden(True)
        self.main.ex2_frame.setHidden(True)
        self.main.param_tabs.setCurrentIndex(0)
        self.main.r_spin.setValue(0.016)
        self.main.q_spin.setValue(1.2)

        self.main.n0_spin.setValue(10000)
        self.main.k0_spin.setValue(11000)
        self.main.t_spin.setValue(250)

        self.main.random_param_check.setChecked(False)

    # Пример 2 -- константный метод
    @Slot()
    def on_sample2(self):
        self.main.ex1_frame.setHidden(True)
        self.main.ex2_frame.setHidden(True)
        self.main.param_tabs.setCurrentIndex(0)

        self.main.r_spin.setValue(0.020)
        self.main.q_spin.setValue(1.9)

        self.main.n0_spin.setValue(10000)
        self.main.k0_spin.setValue(8000)
        self.main.t_spin.setValue(250)

        self.main.random_param_check.setChecked(False)

    # Пример 3 -- дискретный метод
    @Slot()
    def on_sample3(self):
        self.main.ex1_frame.setHidden(True)
        self.main.ex2_frame.setHidden(True)
        self.main.param_tabs.setCurrentIndex(1)

        dc = self.main.discrete_controller
        cur_model = dc.model

        # очистка модели от старых данных
        headers = [
            cur_model.horizontalHeaderItem(i).text()
            for i in range(cur_model.columnCount())
        ]
        cur_model.clear()
        for i, header in enumerate(headers):
            cur_model.setHorizontalHeaderItem(i, QStandardItem(header))

        # fmt: off
        # заполнение новыми данными
        cur_model.insertRow(0, [dc.create_item(val) for val in ["0",   "0,012", "1,16"]])
        cur_model.insertRow(1, [dc.create_item(val) for val in ["115", "0,019", "2,20"]])
        cur_model.insertRow(2, [dc.create_item(val) for val in ["205", "0,008", "1,10"]])
        # fmt: on

        self.main.n0_spin.setValue(10000)
        self.main.k0_spin.setValue(11000)
        self.main.t_spin.setValue(500)

        self.main.random_param_check.setChecked(False)
