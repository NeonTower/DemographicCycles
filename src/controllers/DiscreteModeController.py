from PySide6.QtCore import Slot, QObject, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import *

from src import MainUI

from src.utils import TimeDelegate, FloatDelegate, NumericSortProxyModel


# Часть логики, отвечающая за дискретный режим параметров
class DiscreteModeController(QObject):
    def __init__(self, main: MainUI):
        self.main = main

        # таблица параметров
        self.model = QStandardItemModel(1, 3, self.main)
        self.model.setHorizontalHeaderLabels(["t", "r", "q"])

        # делегаты-валидаторы
        self.t_deleg = TimeDelegate()
        self.r_deleg = FloatDelegate(min_value=0.0, max_value=0.04, decimals=3)
        self.q_deleg = FloatDelegate(min_value=1.0, max_value=3.00, decimals=2)
        self.main.param_view.setItemDelegateForColumn(0, self.t_deleg)
        self.main.param_view.setItemDelegateForColumn(1, self.r_deleg)
        self.main.param_view.setItemDelegateForColumn(2, self.q_deleg)

        # прокси-модель сортировки
        self.proxy_model = NumericSortProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.main.param_view.setModel(self.proxy_model)

        self.main.param_view.setSortingEnabled(True)
        self.main.param_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        # значения по умолчанию
        items = [self.create_item(val) for val in ["0", "0,016", "1,20"]]
        for col, item in enumerate(items):
            self.model.setItem(0, col, item)

        self.main.add_param_button.clicked.connect(self.add_row)
        self.main.remove_param_button.clicked.connect(self.remove_row)

        self.model.itemChanged.connect(self.main.plot_controller.update_plot)

    # Создать ячейку таблицы параметров
    def create_item(self, value):
        item = QStandardItem(str(value))
        item.setFlags(
            Qt.ItemFlag.ItemIsEditable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
        )
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    # Добавить строку со значениями по умолчанию
    @Slot()
    def add_row(self):
        row = self.model.rowCount()
        items = [self.create_item(val) for val in ["0", "0,0", "1,0"]]

        self.model.insertRow(row, items)
        self.main.update_labels()

    # Удалить выбранную строку
    @Slot()
    def remove_row(self):
        selected_indexes = self.main.param_view.selectionModel().selectedIndexes()
        if selected_indexes:
            for index in reversed(sorted(selected_indexes)):
                self.model.removeRow(self.proxy_model.mapToSource(index).row())
            if self.model.rowCount() == 0:
                self.add_row()  # Добавляем стандартную строку, если модель пуста
        else:
            QMessageBox.warning(
                self.main,
                self.tr("Предупреждение"),
                self.tr("Выберите ячейку для удаления строки."),
            )
        self.main.plot_controller.update_plot()
        self.main.update_labels()

    # Получить элементы первого столбца -- моменты времени
    def get_first_column_values(self) -> list[int]:
        first_column_values = []
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item:
                first_column_values.append(int(item.text()))

        return first_column_values

    # Найти ближайший существующий момент времени к заданному
    def find_closest_less_than(self, lst: list[int], target: int) -> int | None:
        less_than_target = [x for x in lst if x <= target]
        if not less_than_target:
            return None
        return max(less_than_target)

    # Получить значение параметра r на интервале, содержащем момент времени t
    def get_discrete_r(self, t: int) -> float:
        try:
            criteria = self.find_closest_less_than(self.get_first_column_values(), t)
            matching_item = self.model.findItems(
                str(criteria), Qt.MatchFlag.MatchExactly, 0
            )[0]
            return float(
                self.model.item(matching_item.row(), 1).text().replace(",", ".")
            )
        except:
            return 0.0

    # Получить значение параметра q на интервале, содержащем момент времени t
    def get_discrete_q(self, t: int) -> float:
        try:
            criteria = self.find_closest_less_than(self.get_first_column_values(), t)
            matching_item = self.model.findItems(
                str(criteria), Qt.MatchFlag.MatchExactly, 0
            )[0]
            return float(
                self.model.item(matching_item.row(), 2).text().replace(",", ".")
            )
        except:
            return 1.0
