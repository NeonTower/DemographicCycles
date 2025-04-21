from PySide6.QtCore import Slot, QTranslator
from PySide6.QtWidgets import *

from src.model import ru_model, en_model
from src.comp import ru_comp, en_comp

from src.autogen.fake import Ui_MainWindow
import src.autogen.res_rc


# Главное окно приложения
class MainUI(QMainWindow, Ui_MainWindow):
    r_scale: bool | None

    def __init__(self):
        super(MainUI, self).__init__()
        self.setupUi(self)

        from src import (
            SampleController,
            ExerciseController,
            DiscreteModeController,
            ScenarioController,
            MathController,
            PlotController,
        )

        self.sample_controller = SampleController(self)
        self.scenario_controller = ScenarioController(self)
        self.math_controller = MathController(self)
        self.plot_controller = PlotController(self)
        self.discrete_controller = DiscreteModeController(self)

        self.r_spin.valueChanged.connect(self.handle_r_spin_edited)
        self.r_slider.valueChanged.connect(self.handle_r_slider_changed)
        self.q_spin.valueChanged.connect(self.handle_q_spin_edited)
        self.q_slider.valueChanged.connect(self.handle_q_slider_changed)

        self.exercise_controller = ExerciseController(self)

        self.translator = QTranslator()
        self.random_frame.setHidden(True)
        self.param_label.setHidden(True)
        self.ex1_frame.setHidden(True)
        self.ex2_frame.setHidden(True)

        self.model_desc_action.triggered.connect(self.show_model)
        self.comp_desc_action.triggered.connect(self.show_comp)
        self.ru_action.triggered.connect(self.on_ru)
        self.en_action.triggered.connect(self.on_en)

        self.about_action.triggered.connect(
            lambda: QMessageBox.about(
                self,
                self.tr("О программе"),
                self.tr("Модель демографических циклов"),
            )
        )

        self.r_scale = None
        self.discrete = False
        self.ru_lang = True

        self.prev_r = self.get_r()
        self.prev_q = self.get_q()

        self.plot_controller.update_plot()
        self.on_ru()

    # Переключить на русский язык
    @Slot()
    def on_ru(self):
        self.translator.load("")
        QApplication.instance().installTranslator(self.translator)
        self.retranslateUi(self)
        self.setWindowTitle("Модель демографических циклов")
        self.exercise_controller.control_ex()
        self.plot_controller.update_plot()
        self.update_labels()
        self.ru_lang = True

    # Переключить на английский язык
    @Slot()
    def on_en(self):
        self.translator.load(":/translations/main_en.qm")
        QApplication.instance().installTranslator(self.translator)
        self.retranslateUi(self)
        self.exercise_controller.control_ex()
        self.plot_controller.update_plot()
        self.update_labels()
        self.ru_lang = False

    # Реакция на переключение режима параметров: константы или события
    @Slot(int)
    def handle_param_mode(self, index):
        self.discrete = False if index == 0 else True
        self.plot_controller.update_plot()
        self.update_labels()

    # Показать описание математической модели
    @Slot()
    def show_model(self):
        model = ru_model(self) if self.ru_lang else en_model(self)
        model.show()

    # Показать описание компьютерной модели
    @Slot()
    def show_comp(self):
        comp = ru_comp(self) if self.ru_lang else en_comp(self)
        comp.show()

    # Обновить строки интерпретации модели
    def update_labels(self):
        period_text, param_text, scenario_text = (
            self.scenario_controller.gen_all_strings()
        )

        self.period_label.setText(period_text)
        self.param_label.setText(param_text)
        self.scenario_label.setText(scenario_text)

    # Согласованность спинбокса и слайдера для r
    @Slot()
    def handle_r_spin_edited(self):
        self.r_scale = True
        self.r_slider.setValue(round(self.r_spin.value() * 1000))

    # Согласованность спинбокса и слайдера для r
    @Slot()
    def handle_r_slider_changed(self):
        self.r_spin.setValue(self.r_slider.value() / 1000)

    # Согласованность спинбокса и слайдера для q
    @Slot()
    def handle_q_spin_edited(self):
        self.r_scale = False
        self.q_slider.setValue(round(self.q_spin.value() * 100))

    # Согласованность спинбокса и слайдера для q
    @Slot()
    def handle_q_slider_changed(self):
        self.q_spin.setValue(self.q_slider.value() / 100)

    # Получить значение параметра r в момент времени t
    def get_r(self, t=0):
        if self.is_discrete():
            return self.discrete_controller.get_discrete_r(t)
        return self.r_spin.value()

    # Получить значение параметра q в момент времени t
    def get_q(self, t=0):
        if self.is_discrete():
            return self.discrete_controller.get_discrete_q(t)
        return self.q_spin.value()

    # N0
    def get_n0(self):
        return self.n0_spin.value()

    # K0
    def get_k0(self):
        return self.k0_spin.value()

    # t
    def get_t(self):
        return self.t_spin.value()

    # Мат. ожидание N
    def get_mo_n(self):
        return self.mo_n_spin.value()

    # Мат. ожидание K
    def get_mo_k(self):
        return self.mo_k_spin.value()

    # Среднеквадр. отклонение N
    def get_sko_n(self):
        return self.sko_n_spin.value()

    # Среднеквадр. отклонение K
    def get_sko_k(self):
        return self.sko_k_spin.value()

    # Использовать рандомные значения?
    def is_randomed(self):
        return self.random_param_check.isChecked()

    # Использовать дискретное задание параметров?
    def is_discrete(self):
        return self.discrete
