from PySide6.QtCore import QObject
from PySide6.QtWidgets import *

from src import MainUI

from enum import Enum


# Соотношение начальных условий систему ДУ
class init_cond(Enum):
    k_great_n = 1
    k_eq_n = 2
    k_less_n = 3


# Динамика параметров при действиях пользователя
class param_dynamics(Enum):
    lowest_params = 4
    params_up = 5
    params_down = 6


# Часть логики, отвечающая за интерпретацию матмодели
class ScenarioController(QObject):
    def __init__(self, main: MainUI):
        self.main = main

    # Сгенерировать интерпретацию текущей ситуации
    def gen_all_strings(self) -> tuple[str, str, str]:
        start_jouken, params_dyn = self.check_scenario()

        if self.main.is_discrete():
            period_text = self.tr(
                "Используется дискретное задание параметров; на интервалах с высокими значениями параметров период демографического цикла будет меньше, и наоборот"
            )
        else:
            period_text = self.gen_period_str(start_jouken, params_dyn)

        param_text = self.gen_param_str(start_jouken, params_dyn)
        scenario_text = self.gen_scen_str(start_jouken, params_dyn)

        return period_text, param_text, scenario_text

    # Проверить состояние системы на основе параметров
    def check_scenario(self) -> tuple[init_cond, param_dynamics]:
        start_jouken = None
        params_dyn = None

        # начальные условия
        if self.main.get_k0() > self.main.get_n0():
            start_jouken = init_cond.k_great_n
        elif self.main.get_k0() == self.main.get_n0():
            start_jouken = init_cond.k_eq_n
        else:
            start_jouken = init_cond.k_less_n

        # динамика параметров
        if self.main.prev_r < self.main.get_r() or self.main.prev_q < self.main.get_q():
            params_dyn = param_dynamics.params_up
        else:
            params_dyn = param_dynamics.params_down

        if self.main.get_r() == 0 or self.main.get_q() == 1.0:
            params_dyn = param_dynamics.lowest_params

        self.main.prev_r = self.main.get_r()
        self.main.prev_q = self.main.get_q()

        return start_jouken, params_dyn

    # Интерпретация действий пользователя и реакции системы
    def gen_period_str(self, start: init_cond, dyn: param_dynamics) -> str:
        if dyn == param_dynamics.lowest_params:
            period_str = self.tr(
                "Показатели не имеют периодического характера из-за выбранных значений параметров"
            )
        elif start == init_cond.k_eq_n:
            if self.main.is_randomed():
                period_str = self.tr(
                    "Использованы случайные значения, поэтому система выходит из точки равновесия, период приблизительно равен ситуации без внесения случайности"
                )
            else:
                period_str = self.tr(
                    "Показатели не имеют периодического характера из-за выбранных начальных условий – система находится в точке равновесия"
                )
        else:
            period_str = self.tr(
                "Ожидаемый период демографического цикла = %i лет"
            ) % (self.main.math_controller.calc_period())
            if self.main.r_scale is not None:
                if dyn == param_dynamics.params_up:
                    period_str = self.tr(
                        'Увеличился параметр модели – произошло увеличение потребления и ускорение истощения ресурсов, период <span style=" text-decoration: underline; color:#ff0000;">уменьшился</span>; ожидаемый период демографического цикла = %i лет'
                    ) % (self.main.math_controller.calc_period())
                else:
                    period_str = self.tr(
                        'Уменьшился параметр модели – произошло снижение потребления и замедление истощения ресурсов, период <span style=" text-decoration: underline; color:#30aa70;">увеличился</span>; ожидаемый период демографического цикла = %i лет'
                    ) % (self.main.math_controller.calc_period())
        return period_str

    # Описание изменённого параметра
    def gen_param_str(self, start: init_cond, dyn: param_dynamics) -> str:
        r_description = self.tr(
            "Параметр r обозначает максимальный естественный прирост населения в благоприятных условиях."
        )
        q_description = self.tr(
            "Параметр q показывает, сколько человек (включая и себя) может в благоприятных условиях прокормить один земледелец (или сколько семей может прокормить одна земледельческая семья). "
        )

        if self.main.r_scale:
            param_str = (
                self.tr(
                    "Изменён параметр r, его значения обычно находятся в пределах 0.01 &le; r &le; 0.02. "
                )
                + r_description
            )
        elif self.main.r_scale is not None:
            param_str = (
                self.tr(
                    "Изменён параметр q, его значения обычно колеблются в пределах 1.2 &le; q &le; 2.0. "
                )
                + q_description
            )
        else:
            param_str = self.main.param_label.text()
        return param_str

    # Интерпретация сценария при начальных условиях системы
    def gen_scen_str(self, start: init_cond, dyn: param_dynamics) -> str:
        if dyn == param_dynamics.lowest_params:
            scen_str = self.tr(
                "Такие параметры не влияют на динамику населения и ресурсов, система не имеет колебаний независимо от начальных условий"
            )
        elif start == init_cond.k_great_n:
            scen_str = self.tr(
                "Начальные запасы были больше необходимого населению, наблюдается рост населения и снижение количества припасов"
            )
            if self.main.is_randomed():
                scen_str += self.tr(
                    "; случайные колебания могут как замедлить наступление кризиса, так и ускорить"
                )
        elif start == init_cond.k_less_n:
            scen_str = self.tr(
                "Начальные запасы были меньше необходимого населению, наблюдается гибель части населения и постепеное увеличение количества припасов"
            )
            if self.main.is_randomed():
                scen_str += self.tr(
                    "; случайные колебания могут как замедлить наступление кризиса, так и ускорить"
                )
        elif start == init_cond.k_eq_n:
            scen_str = self.tr(
                "Начальных запасов ровно хватает для населения, это точка равновесия системы"
            )
            if self.main.is_randomed():
                scen_str += self.tr(
                    ", но случайные колебания выводят систему из этого состояния, начинаются колебания параметров"
                )

        return scen_str
