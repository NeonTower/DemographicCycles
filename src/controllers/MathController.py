from src import MainUI

import numpy as np
from scipy.integrate import solve_ivp


# Часть логики, отвечающая за математические операции
class MathController:
    def __init__(self, main: MainUI):
        self.main = main

    # Решить систему ОДУ
    def solve(self) -> dict:
        t_max = self.main.get_t()

        # начальные условия
        N_0 = self.main.get_n0()
        K_0 = self.main.get_k0()

        y0 = [N_0, K_0]

        # функция, которая описывает систему ДУ
        def system(t, y):
            N, K = y

            r = self.main.get_r(t)
            q = self.main.get_q(t)

            # случайные величины
            if self.main.is_randomed():
                random_N = (
                    np.random.normal(self.main.get_mo_n(), self.main.get_sko_n(), 1)[0]
                    if round(t) % 5 == 0
                    else 1.0
                )
                random_K = (
                    np.random.normal(self.main.get_mo_k(), self.main.get_sko_k(), 1)[0]
                    if round(t) % 5 == 0
                    else 1.0
                )

                N *= random_N
                K *= random_K

            # fmt: off
            dN = r * N * (1 - N / K) 
            dK = N_0 * q * N / (N * q - N + N_0) - N 
            # fmt: on

            return [dN, dK]

        # интервал времени для решения
        t_span = (0, t_max)
        t_eval = np.linspace(t_span[0], t_span[1], t_max, dtype=int)

        # решение системы ДУ
        solution = solve_ivp(system, t_span, y0, t_eval=t_eval)
        return solution  # type: ignore

    # Вычислить период демографического цикла по текущим параметрам
    def calc_period(self) -> float:
        r = self.main.get_r()
        q = self.main.get_q()
        D = r**2 / 4 - r * (1 - 1 / q)
        return 2 * np.pi / np.sqrt(np.abs(D))
