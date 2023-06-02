import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from math import *
from random import randint


# начальные значения
phase = [randint(0, 628) / 100 for i in range(6)]  # начальные фазы
N = 6  # количество осцилляторов
K_multiplier = 1  # множитель коэффициента взаимодействия
K_natural = 1  # коэффициент взаимодействия
R = 2  # условный радиус хоровода
speed = [(1 + randint(-3, 3) / 10) for i in range(6)]
freq = [(speed[i] / (R * 2 * pi)) for i in range(6)]
cur_xmin = 0
cur_xmax = 1000
cur_ymin = 0
cur_ymax = 100


def updateGraph(limit: int, steps: int):
    t = np.linspace(0, limit, steps)
    w = odeint(f, phase, t)
    y1 = w[:, 0]
    y2 = w[:, 1]
    y3 = w[:, 2]
    y4 = w[:, 3]
    y5 = w[:, 4]
    y6 = w[:, 5]
    graph_axes.clear()
    graph_axes.plot(t, y1, '-o', t, y2, '-o', t, y3, '-o', t, y4, '-o', t, y5, '-o', t, y6, '-o', linewidth=2)
    graph_axes.grid(1)
    graph_axes.set_xlim(cur_xmin, cur_xmax)
    graph_axes.set_ylim(cur_ymin, cur_ymax)
    plt.draw()


def new_phases(value):
    global phase
    phase = [randint(0, 628) / 100 for i in range(6)]
    updateGraph(1000, 500)


def new_rad(value):
    global freq
    global R
    if value != '':
        R = int(value)
    freq = [(speed[i] / (R * 2 * pi)) for i in range(6)]
    updateGraph(1000, 500)


def f(y, t):
    K = K_natural * K_multiplier
    y1, y2, y3, y4, y5, y6 = y
    return [freq[0] + 1 / N * (K * sin(y2 - y1) + K / 3 * (sin(y6 - y1))),
            freq[1] + 1 / N * (K * sin(y3 - y2) + K * (sin(y1 - y2))),
            freq[2] + 1 / N * (K * sin(y4 - y3) + K * (sin(y2 - y3))),
            freq[3] + 1 / N * (K * sin(y5 - y4) + K * (sin(y3 - y4))),
            freq[4] + 1 / N * (K / 3 * sin(y6 - y5) + K * (sin(y4 - y5))),
            freq[5] + 1 / N * (K / 3 * sin(y1 - y6) + K / 3 * (sin(y5 - y6)))]


def limchng(val):
    global cur_xmax, cur_xmin, cur_ymax, cur_ymin
    x_min = cur_xmin
    x_max = cur_xmax
    y_min = cur_ymin
    y_max = cur_ymax
    if tb_xmin.text != '':
        x_min = int(tb_xmin.text)
        cur_xmin = x_min
    if tb_xmax.text != '':
        x_max = int(tb_xmax.text)
        cur_xmax = x_max
    if tb_ymax.text != '':
        y_max = int(tb_ymax.text)
        cur_ymax = y_max
    if tb_ymin.text != '':
        y_min = int(tb_ymin.text)
        cur_ymin = y_min
    graph_axes.set_xlim(x_min, x_max)
    graph_axes.set_ylim(y_min, y_max)
    plt.draw()


def tb_change(value):
    global K_natural
    if value != '':
        K_natural = float(value)
    updateGraph(1000, 500)


# построение графика
fig, graph_axes = plt.subplots()
fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)

updateGraph(1000, 500)

axes_tb1 = plt.axes([0.4, 0.01, 0.4, 0.05])
tb_K = TextBox(axes_tb1, "Значение K")
tb_K.on_text_change(tb_change)


axes_tb2 = plt.axes([0.1, 0.01, 0.1, 0.05])
tb_xmin = TextBox(axes_tb2, "X min")
tb_xmin.on_text_change(limchng)

axes_tb3 = plt.axes([0.1, 0.07, 0.1, 0.05])
tb_xmax = TextBox(axes_tb3, "X max")
tb_xmax.on_text_change(limchng)

axes_tb4 = plt.axes([0.4, 0.13, 0.4, 0.05])
tb_R = TextBox(axes_tb4, "Значение R")
tb_R.on_text_change(new_rad)

axes_tb6 = plt.axes([0.1, 0.19, 0.1, 0.05])
tb_ymin = TextBox(axes_tb6, "Y min")
tb_ymin.on_text_change(limchng)

axes_tb5 = plt.axes([0.1, 0.25, 0.1, 0.05])
tb_ymax = TextBox(axes_tb5, "Y max")
tb_ymax.on_text_change(limchng)

axes_button = plt.axes([0.4, 0.19, 0.1, 0.1])
btn = Button(axes_button, "New start phases")
btn.on_clicked(new_phases)

plt.draw()
plt.show()
