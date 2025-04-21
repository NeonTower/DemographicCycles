from PySide6.QtCore import Slot, QObject

from src import MainUI


# Часть логики, отвечающая за поведение упражнений
class ExerciseController(QObject):
    def __init__(self, main: MainUI):
        self.main = main

        self.main.ex1_action.triggered.connect(self.on_ex1_trigger)
        self.main.ex2_action.triggered.connect(self.on_ex2_trigger)
        self.main.r_slider.valueChanged.connect(self.control_ex)
        self.main.q_slider.valueChanged.connect(self.control_ex)

        self.main.param_tabs.currentChanged.connect(self.main.handle_param_mode)
        self.main.param_tabs.currentChanged.connect(self.control_ex)
        self.main.n0_spin.valueChanged.connect(self.control_ex)
        self.main.k0_spin.valueChanged.connect(self.control_ex)
        self.main.random_param_check.stateChanged.connect(self.control_ex)

    # Обновить состояние упражнений -- текст, выполнение
    @Slot()
    def control_ex(self):
        from src import init_cond, param_dynamics

        start_jouken, params_dyn = self.main.scenario_controller.check_scenario()
        good_status = self.tr(
            '<span style=" text-decoration: underline; color:#30aa70;">Выполнено</span>'
        )
        bad_status = self.tr(
            '<span style=" text-decoration: underline; color:#ff0000;">Не выполнено</span>'
        )

        # дискретный режим, выполнение недоступно
        if self.main.is_discrete():
            ex1_text = self.tr(
                "Для выполнения упражнения необходимо выбрать другой метод задания параметров"
            )
            ex2_text = ex1_text

            self.main.ex1_label.setText(ex1_text)
            self.main.ex2_label.setText(ex2_text)

            self.main.ex1_status_label.setText(bad_status)
            self.main.ex2_status_label.setText(bad_status)

            return

        # случайные величины, выполнение недоступно
        if self.main.is_randomed():
            ex1_text = self.tr("Для выполнения упражнения нельзя использовать случайные величины")
            ex2_text = ex1_text

            self.main.ex1_label.setText(ex1_text)
            self.main.ex2_label.setText(ex2_text)

            self.main.ex1_status_label.setText(bad_status)
            self.main.ex2_status_label.setText(bad_status)

            return

        # крайние случаи параметров
        if (
            start_jouken == init_cond.k_eq_n
            or params_dyn == param_dynamics.lowest_params
        ):
            ex1_text = self.tr("Для выполнения упражнения показатели должны иметь периодический характер")
            ex2_text = ex1_text

            self.main.ex1_label.setText(ex1_text)
            self.main.ex2_label.setText(ex2_text)

            self.main.ex1_status_label.setText(bad_status)
            self.main.ex2_status_label.setText(bad_status)

            return

        # расчёт и проверка
        if (
            start_jouken != init_cond.k_eq_n
            and params_dyn != param_dynamics.lowest_params
        ):
            ex1_text = self.tr("Упражнение 1: подберите такие значения параметров, чтобы период демографического цикла составлял менее 50 лет")
            ex2_text = self.tr(
                "Упражнение 2: подберите такие значения параметров, чтобы период демографического цикла составлял более 200 лет"
            )

            self.main.ex1_label.setText(ex1_text)
            self.main.ex2_label.setText(ex2_text)

            period = self.main.math_controller.calc_period()
            if period < 50:
                self.main.ex1_status_label.setText(good_status)
            else:
                self.main.ex1_status_label.setText(bad_status)
            if period > 200:
                self.main.ex2_status_label.setText(good_status)
            else:
                self.main.ex2_status_label.setText(bad_status)

            return
        raise RuntimeError()

    # Показать первое упражнение
    @Slot()
    def on_ex1_trigger(self):
        self.main.ex1_frame.setVisible(True)
        self.main.ex2_frame.setVisible(False)

    # Показать второе упражнение
    @Slot()
    def on_ex2_trigger(self):
        self.main.ex1_frame.setVisible(False)
        self.main.ex2_frame.setVisible(True)
