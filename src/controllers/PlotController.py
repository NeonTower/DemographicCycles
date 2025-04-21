from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from src import MainUI


# Часть логики, отвечающая за отображение графиков
class PlotController(QObject):
    def __init__(self, main: MainUI):
        self.main = main

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.toolbar = NavigationToolbar(self.canvas, self.main.plot_frame)

        self.main.plot_frame.layout().insertWidget(0, self.toolbar)
        self.main.plot_frame.layout().insertWidget(1, self.canvas)

        self.main.r_spin.valueChanged.connect(self.update_plot)
        self.main.q_spin.valueChanged.connect(self.update_plot)
        self.main.mo_n_spin.valueChanged.connect(self.update_plot)
        self.main.mo_k_spin.valueChanged.connect(self.update_plot)
        self.main.sko_n_spin.valueChanged.connect(self.update_plot)
        self.main.sko_k_spin.valueChanged.connect(self.update_plot)
        self.main.n0_spin.valueChanged.connect(self.update_plot)
        self.main.k0_spin.valueChanged.connect(self.update_plot)
        self.main.t_spin.valueChanged.connect(self.update_plot)
        self.main.n_check.stateChanged.connect(self.update_plot)
        self.main.k_check.stateChanged.connect(self.update_plot)
        self.main.random_param_check.stateChanged.connect(self.update_plot)

    # Решить систему ОДУ и обновить график
    @Slot()
    def update_plot(self):
        self.figure.clear()
        sol = self.main.math_controller.solve()

        ax = self.figure.add_subplot(111)
        if self.main.n_check.isChecked():
            ax.plot(
                sol.t,
                sol.y[0],
                label=self.tr("N – численность населения"),
                color="blue",
            )
        if self.main.k_check.isChecked():
            ax.plot(
                sol.t,
                sol.y[1],
                label=self.tr("K – запасы зерна на человека"),
                color="green",
            )
        ax.set_xlabel(self.tr("Время"), fontsize=12)
        ax.set_ylabel(self.tr("Доля населения"), fontsize=12)
        ax.set_title(self.tr("Модель демографических циклов"), fontsize=14)
        ax.legend()
        ax.grid(True)

        self.canvas.draw()
        self.main.update_labels()
