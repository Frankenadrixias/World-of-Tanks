# -* coding: utf-8 *-
"""
@File：fire_gui.py
@Time：2023/2/19 11:22
@Auth：FriedrichXR
@IDE ：PyCharm
@desc：WoT calculator on PyQt5 by 黯流雾雨
"""

from PyQt5.QtWidgets import *
import sys
import csv
from fire_ui import Ui_MainWindow
import numpy as np
import matplotlib
from matplotlib.pylab import mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from math import sqrt, log

matplotlib.use("Qt5Agg")  # 声明使用QT5
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示
font = {'family': 'Microsoft Yahei'}  # 设置字体
matplotlib.rc('font', **font)

# 配件属性，每个配件都会对以下属性中的某一个或某几个产生影响：
# 瞄准时间 aim_time，基础精度 dispersion，三扩系数 factors，转向速度 traverse_speed
# 每行数字分别代表白装/1级橙、加成槽/2级橙、红装/3级橙、紫装对以上四种属性的作用数值
item_level = [[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],  # 无配件
              [[1, 1, 0.8, 1], [1, 1, 0.77, 1], [1, 1, 0.75, 1], [1, 1, 0.725, 1]],  # 垂稳
              [[1.1, 1, 1, 1], [1.115, 1, 1, 1], [1.125, 1, 1, 1], [1.135, 1, 1, 1]],  # 炮控
              [[1, 1, 0.9, 1.1], [1, 1, 0.875, 1.125], [1, 1, 0.85, 1.15], [1, 1, 0.825, 1.175]],  # 旋转
              [[1, 0.95, 1, 1], [1, 0.93, 1, 1], [1, 0.92, 1, 1], [1, 1, 1, 1]],  # 瞄具
              [[1.0227, 0.9778, 1, 1.0227], [1.0272, 0.9735, 1, 1.0272],  # 通风
               [1.0340, 0.9671, 1, 1.0340], [1.0385, 0.9629, 1, 1.0385]],
              [[1.06, 1, 0.93, 1], [1.07, 1, 0.91, 1], [1.09, 1, 0.89, 1], [1, 1, 1, 1]],  # 火控
              [[1, 1, 0.96, 1.04], [1, 1, 0.95, 1.05], [1, 1, 0.94, 1.06], [1, 1, 1, 1]]]  # 机动


# 创建一个matplotlib图形绘制类
class MyFigure(FigureCanvasQTAgg):
    def __init__(self, width=4, height=3, dpi=120):

        # 创建一个 Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        # 在父类中激活Figure窗口
        super(MyFigure, self).__init__(self.fig)

        # 定义子图，用于绘制图形
        self.axes1, self.axes2, self.axes3, self.axes4 = None, None, None, None

        # Matplotlib根据输入参数画图

    def plot_figure(self, f_move, f_hull, f_gun, f_fire, t0, d0, d_obj, v0, w_hull, w_gun, t_r,
                    check, angle, i1, i2, i3, l1, l2, l3, i4, i5, i6, l4, l5, l6):

        # 重置和调整画布
        self.fig.clf()
        self.fig.subplots_adjust(left=0.06, bottom=0.08, right=0.98, top=0.95,
                                 hspace=0.3, wspace=0.16)

        # 计算配件影响的参数数值
        t_item_1 = item_level[i1][l1][0] * item_level[i2][l2][0] * item_level[i3][l3][0]
        d_item_1 = item_level[i1][l1][1] * item_level[i2][l2][1] * item_level[i3][l3][1]
        f_item_1 = item_level[i1][l1][2] * item_level[i2][l2][2] * item_level[i3][l3][2]
        w_item_1 = item_level[i1][l1][3] * item_level[i2][l2][3] * item_level[i3][l3][3]

        t_item_2 = item_level[i4][l4][0] * item_level[i5][l5][0] * item_level[i6][l6][0]
        d_item_2 = item_level[i4][l4][1] * item_level[i5][l5][1] * item_level[i6][l6][1]
        f_item_2 = item_level[i4][l4][2] * item_level[i5][l5][2] * item_level[i6][l6][2]
        w_item_2 = item_level[i4][l4][3] * item_level[i5][l5][3] * item_level[i6][l6][3]

        # 图1：坦克直线前进时火炮缩圈到指定精度所需时间与当前速度的关系图
        self.axes1 = self.fig.add_subplot(221)
        x, y1, y2, y3, y4 = [], [], [], [], []
        for i in range(0, int(v0) * 100):
            x.append(i / 100.0)
            t1 = (t0 / t_item_1) * log(d_item_1 * sqrt(1 + (x[i] * f_move * f_item_1) ** 2))
            y1.append(t1 if t1 >= 0 else 0)
            t2 = (t0 / t_item_1) * log((d0 * d_item_1) * (sqrt(1 + (x[i] * f_move * f_item_1) ** 2)) / d_obj)
            y2.append(t2 if t2 >= 0 else 0)
            t3 = (t0 / t_item_2) * log(d_item_2 * sqrt(1 + (x[i] * f_move * f_item_2) ** 2))
            y3.append(t3 if t3 >= 0 else 0)
            t4 = (t0 / t_item_2) * log((d0 * d_item_2) * (sqrt(1 + (x[i] * f_move * f_item_2) ** 2)) / d_obj)
            y4.append(t4 if t4 >= 0 else 0)

        self.axes1.plot(x, y1, linestyle=':', label='缩圈到基础精度（配件组1）')
        self.axes1.plot(x, y2, linestyle=':', label='缩圈到目标精度（配件组1）')
        self.axes1.plot(x, y3, label='缩圈到基础精度（配件组2）')
        self.axes1.plot(x, y4, label='缩圈到目标精度（配件组2）')
        self.axes1.set_title("坦克直线前进时火炮缩圈到指定精度所需时间与当前速度的关系")
        self.axes1.set_ylabel("缩圈所需时间(s)", fontsize=10, labelpad=3)
        self.axes1.set_xlabel("当前移动速度(km/h)", fontsize=10, labelpad=2)
        self.axes1.grid(which='major', linestyle=':', linewidth=0.5)
        self.axes1.legend(fontsize=9)
        self.axes1.patch.set_facecolor("gray")
        self.axes1.patch.set_alpha(0.05)

        # 图2：坦克直线前进时火炮实时精度与当前速度的关系图
        self.axes2 = self.fig.add_subplot(222)
        x, y1, y2, y3, y4 = [], [], [], [], []
        for i in range(0, int(v0) * 100):
            x.append(i / 100.0)
            t1 = d0 * d_item_1 * (sqrt(1 + (x[i] * f_move * f_item_1) ** 2))
            y1.append(t1 if t1 >= d0 * d_item_1 else d0 * d_item_1)
            t2 = d0 * d_item_2 * (sqrt(1 + (x[i] * f_move * f_item_2) ** 2))
            y2.append(t2 if t2 >= d0 * d_item_2 else d0 * d_item_2)
            y3.append(d_obj)
            y4.append(d0)

        self.axes2.plot(x, y1, label='实时精度（配件组1）')
        self.axes2.plot(x, y2, label='实时精度（配件组2）')
        self.axes2.plot(x, y3, linewidth=1, linestyle='--',
                        label='目标精度: ' + str('{:.3f}'.format(y3[-1])) + 'm')
        self.axes2.plot(x, y4, linewidth=1, linestyle='--',
                        label='基础精度: ' + str('{:.3f}'.format(y4[-1])) + 'm')
        self.axes2.set_title("坦克直线前进时火炮实时精度与当前速度的关系")
        self.axes2.set_ylabel("当前实时精度(m)", fontsize=10, labelpad=3)
        self.axes2.set_xlabel("当前移动速度(km/h)", fontsize=10, labelpad=2)
        self.axes2.grid(which='major', linestyle=':', linewidth=0.5)
        self.axes2.legend(fontsize=9)
        self.axes2.patch.set_facecolor("gray")
        self.axes2.patch.set_alpha(0.05)

        # 图3：坦克旋转时火炮缩圈到指定精度所需时间与旋转角度的关系图
        self.axes3 = self.fig.add_subplot(223)
        x, y1, y2, y3, y4 = [], [], [], [], []
        for i in range(0, angle + 1):
            x.append(i)

            # 如果勾选 “旋转车体” 选项：
            if check is True:
                t1 = (t0 / t_item_1) * log(d_item_1 * sqrt(1 + ((w_gun * w_item_1 * f_gun) ** 2 +
                                                                (w_hull * w_item_1 * f_hull) ** 2) * f_item_1 ** 2))
                t2 = (t0 / t_item_1) * log((d0 * d_item_1) *
                                           (sqrt(1 + ((w_gun * w_item_1 * f_gun) ** 2 +
                                                      (w_hull * w_item_1 * f_hull) ** 2) * f_item_1 ** 2)) / d_obj)
                t3 = (t0 / t_item_2) * log(d_item_2 * sqrt(1 + ((w_gun * w_item_2 * f_gun) ** 2 +
                                                                (w_hull * w_item_2 * f_hull) ** 2) * f_item_2 ** 2))
                t4 = (t0 / t_item_2) * log((d0 * d_item_2) *
                                           (sqrt(1 + ((w_gun * w_item_2 * f_gun) ** 2 +
                                                      (w_hull * w_item_2 * f_hull) ** 2) * f_item_2 ** 2)) / d_obj)
                y1.append(i / ((w_gun + w_hull) * w_item_1) + t1)
                y2.append(i / ((w_gun + w_hull) * w_item_1) + t2)
                y3.append(i / ((w_gun + w_hull) * w_item_2) + t3)
                y4.append(i / ((w_gun + w_hull) * w_item_2) + t4)

            # 不勾选 “旋转车体” 选项：
            else:
                t1 = (t0 / t_item_1) * log(d_item_1 * sqrt(1 + (w_gun * w_item_1 * f_gun * f_item_1) ** 2))
                t2 = (t0 / t_item_1) * log((d0 * d_item_1) *
                                           (sqrt(1 + (w_gun * w_item_1 * f_gun * f_item_1) ** 2)) / d_obj)
                t3 = (t0 / t_item_2) * log(d_item_2 * sqrt(1 + (w_gun * w_item_2 * f_gun * f_item_2) ** 2))
                t4 = (t0 / t_item_2) * log((d0 * d_item_2) *
                                           (sqrt(1 + (w_gun * w_item_2 * f_gun * f_item_2) ** 2)) / d_obj)
                y1.append(i / (w_gun * w_item_1) + t1)
                y2.append(i / (w_gun * w_item_1) + t2)
                y3.append(i / (w_gun * w_item_2) + t3)
                y4.append(i / (w_gun * w_item_2) + t4)

        self.axes3.plot(x, y1, linestyle=':', label='缩圈到基础精度（配件组1）')
        self.axes3.plot(x, y2, linestyle=':', label='缩圈到目标精度（配件组1）')
        self.axes3.plot(x, y3, label='缩圈到基础精度（配件组2）')
        self.axes3.plot(x, y4, label='缩圈到目标精度（配件组2）')
        self.axes3.set_title("坦克旋转时火炮缩圈到指定精度所需时间与旋转角度的关系")
        self.axes3.set_ylabel("缩圈所需时间(s)", fontsize=10, labelpad=3)
        self.axes3.set_xlabel("旋转角度(°)", fontsize=10, labelpad=2)
        self.axes3.grid(which='major', linestyle=':', linewidth=0.5)
        self.axes3.legend(fontsize=9)
        self.axes3.patch.set_facecolor("gray")
        self.axes3.patch.set_alpha(0.05)

        # 图4：坦克开火后火炮实时精度与开火后经过时间的关系图
        self.axes4 = self.fig.add_subplot(224)
        x, y1, y2, y3, y4 = [], [], [], [], []
        for i in range(0, int(t_r * 100)):
            x.append(i / 100.0)
            if x[i] == 0:
                t1 = d0 * d_item_1
                t2 = d0 * d_item_2
            else:
                t1 = d0 * d_item_1 * (sqrt(1 + (f_fire * f_item_1) ** 2)) / np.e ** (x[i] * t_item_1 / t0)
                t2 = d0 * d_item_2 * (sqrt(1 + (f_fire * f_item_2) ** 2)) / np.e ** (x[i] * t_item_2 / t0)
            y1.append(t1 if t1 >= d0 * d_item_1 else d0 * d_item_1)
            y2.append(t2 if t2 >= d0 * d_item_2 else d0 * d_item_2)
            y3.append(d_obj)
            y4.append(d0)

        self.axes4.plot(x, y1, label='实时精度（配件组1）')
        self.axes4.plot(x, y2, label='实时精度（配件组2）')
        self.axes4.plot(x, y3, linewidth=1, linestyle='--',
                        label='目标精度: ' + str('{:.3f}'.format(y3[-1])) + 'm')
        self.axes4.plot(x, y4, linewidth=1, linestyle='--',
                        label='基础精度: ' + str('{:.3f}'.format(y4[-1])) + 'm')
        self.axes4.set_title("坦克开火后火炮实时精度与开火后经过时间的关系")
        self.axes4.set_ylabel("当前实时精度(m)", fontsize=10, labelpad=3)
        self.axes4.set_xlabel("开火后经过时间(s)", fontsize=10, labelpad=2)
        self.axes4.grid(which='major', linestyle=':', linewidth=0.5)
        self.axes4.legend(fontsize=9)
        self.axes4.patch.set_facecolor("gray")
        self.axes4.patch.set_alpha(0.05)

        # 画布重绘和刷新
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


# 继承 QMainWindow类和 Ui_MainWindow界面类
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.canvas = MyFigure(width=5, height=4, dpi=100)
        self.plot_fig()

        # 在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox，对ui界面内的groupBox控件进行操作
        self.gridlayout.addWidget(self.canvas)

    # 点击计算数据 Button 触发
    def click_button(self):

        # 基础扩圈系数
        move_f = self.horizontalSlider_move.value() / 100.0
        rotate_f = self.horizontalSlider_rotate.value() / 100.0
        gun_f = self.horizontalSlider_gun.value() / 100.0
        fire_f = self.doubleSpinBox_fire.value()

        # 瞄准时间和精度
        aim_time = self.doubleSpinBox_aimTime.value()
        dispersion = self.doubleSpinBox_dispersion.value()
        dispersion_obj = self.doubleSpinBox_objectDispersion.value()

        # 极速和旋转速度
        top_speed = self.doubleSpinBox_topSpeed.value()
        hull_speed = self.doubleSpinBox_hullSpeed.value()
        turret_speed = self.doubleSpinBox_turretSpeed.value()

        # 是否勾选同时旋转车体和旋转角度
        check = self.radioButton.isChecked()
        angle = self.spinBox.value()

        # 配件选择下拉菜单
        # 第一套配件的选择结果
        item_1 = self.comboBox_item_1.currentIndex()
        item_2 = self.comboBox_item_2.currentIndex()
        item_3 = self.comboBox_item_3.currentIndex()
        level_1 = self.comboBox_level_1.currentIndex()
        level_2 = self.comboBox_level_2.currentIndex()
        level_3 = self.comboBox_level_3.currentIndex()

        # 第二套配件的选择结果
        item_4 = self.comboBox_item_4.currentIndex()
        item_5 = self.comboBox_item_5.currentIndex()
        item_6 = self.comboBox_item_6.currentIndex()
        level_4 = self.comboBox_level_4.currentIndex()
        level_5 = self.comboBox_level_5.currentIndex()
        level_6 = self.comboBox_level_6.currentIndex()

        # 配件装备信息文本
        txt_1 = self.comboBox_item_1.currentText() + '(' + self.comboBox_level_1.currentText() + ')'
        txt_2 = self.comboBox_item_2.currentText() + '(' + self.comboBox_level_2.currentText() + ')'
        txt_3 = self.comboBox_item_3.currentText() + '(' + self.comboBox_level_3.currentText() + ')'
        txt_4 = self.comboBox_item_4.currentText() + '(' + self.comboBox_level_4.currentText() + ')'
        txt_5 = self.comboBox_item_5.currentText() + '(' + self.comboBox_level_5.currentText() + ')'
        txt_6 = self.comboBox_item_6.currentText() + '(' + self.comboBox_level_6.currentText() + ')'

        # 配件影响属性
        t_item_1 = item_level[item_1][level_1][0] * item_level[item_2][level_2][0] * item_level[item_3][level_3][0]
        d_item_1 = item_level[item_1][level_1][1] * item_level[item_2][level_2][1] * item_level[item_3][level_3][1]
        f_item_1 = item_level[item_1][level_1][2] * item_level[item_2][level_2][2] * item_level[item_3][level_3][2]
        w_item_1 = item_level[item_1][level_1][3] * item_level[item_2][level_2][3] * item_level[item_3][level_3][3]

        t_item_2 = item_level[item_4][level_4][0] * item_level[item_5][level_5][0] * item_level[item_6][level_6][0]
        d_item_2 = item_level[item_4][level_4][1] * item_level[item_5][level_5][1] * item_level[item_6][level_6][1]
        f_item_2 = item_level[item_4][level_4][2] * item_level[item_5][level_5][2] * item_level[item_6][level_6][2]
        w_item_2 = item_level[item_4][level_4][3] * item_level[item_5][level_5][3] * item_level[item_6][level_6][3]

        # 计算各个状态下的数值
        # 坦克直线前进时火炮缩圈到指定精度所需时间与最大精度
        t1 = (aim_time / t_item_1) * log(d_item_1 * sqrt(1 + (top_speed * move_f * f_item_1) ** 2))
        t2 = (aim_time / t_item_1) * log((dispersion * d_item_1) *
                                         (sqrt(1 + (top_speed * move_f * f_item_1) ** 2)) / dispersion_obj)
        t3 = (dispersion * d_item_1) * (sqrt(1 + (top_speed * move_f * f_item_1) ** 2))

        t4 = (aim_time / t_item_2) * log(d_item_2 * sqrt(1 + (top_speed * move_f * f_item_2) ** 2))
        t5 = (aim_time / t_item_2) * log((dispersion * d_item_2) *
                                         (sqrt(1 + (top_speed * move_f * f_item_2) ** 2)) / dispersion_obj)
        t6 = (dispersion * d_item_2) * (sqrt(1 + (top_speed * move_f * f_item_2) ** 2))

        # 坦克旋转时火炮缩圈到指定精度所需时间与旋转角度
        if check is True:
            t7 = angle / ((turret_speed + hull_speed) * w_item_1) + (aim_time / t_item_1) * \
                 log(d_item_1 * sqrt(1 + ((turret_speed * w_item_1 * gun_f) ** 2 +
                                          (hull_speed * w_item_1 * rotate_f) ** 2) * f_item_1 ** 2))
            t8 = angle / ((turret_speed + hull_speed) * w_item_1) + (aim_time / t_item_1) * \
                 log((dispersion * d_item_1) *
                     (sqrt(1 + ((turret_speed * w_item_1 * gun_f) ** 2 +
                                (hull_speed * w_item_1 * rotate_f) ** 2) * f_item_1 ** 2)) / dispersion_obj)

            t9 = angle / ((turret_speed + hull_speed) * w_item_2) + (aim_time / t_item_2) * \
                 log(d_item_1 * sqrt(1 + ((turret_speed * w_item_2 * gun_f) ** 2 +
                                          (hull_speed * w_item_2 * rotate_f) ** 2) * f_item_2 ** 2))
            t10 = angle / ((turret_speed + hull_speed) * w_item_2) + (aim_time / t_item_2) * \
                  log((dispersion * d_item_2) *
                      (sqrt(1 + ((turret_speed * w_item_2 * gun_f) ** 2 +
                                 (hull_speed * w_item_2 * rotate_f) ** 2) * f_item_2 ** 2)) / dispersion_obj)
        else:
            t7 = angle / (turret_speed * w_item_1) + (aim_time / t_item_1) * \
                 log(d_item_1 * sqrt(1 + (turret_speed * w_item_1 * gun_f * f_item_1) ** 2))
            t8 = angle / (turret_speed * w_item_1) + (aim_time / t_item_1) * \
                 log((dispersion * d_item_1) *
                     (sqrt(1 + (turret_speed * w_item_1 * gun_f * f_item_1) ** 2)) / dispersion_obj)

            t9 = angle / (turret_speed * w_item_2) + (aim_time / t_item_2) * \
                 log(d_item_2 * sqrt(1 + (turret_speed * w_item_2 * gun_f * f_item_2) ** 2))
            t10 = angle / (turret_speed * w_item_2) + (aim_time / t_item_2) * \
                  log((dispersion * d_item_2) *
                      (sqrt(1 + (turret_speed * w_item_2 * gun_f * f_item_2) ** 2)) / dispersion_obj)

        # 坦克开火后火炮完整缩圈时间
        t11 = (aim_time / t_item_1) * log(d_item_1 * sqrt(1 + (fire_f * f_item_1) ** 2))
        t12 = (aim_time / t_item_1) * log((dispersion * d_item_1) *
                                          (sqrt(1 + (fire_f * f_item_1) ** 2)) / dispersion_obj)
        t13 = (aim_time / t_item_2) * log(d_item_2 * sqrt(1 + (fire_f * f_item_2) ** 2))
        t14 = (aim_time / t_item_2) * log((dispersion * d_item_2) *
                                          (sqrt(1 + (fire_f * f_item_2) ** 2)) / dispersion_obj)

        # 显示信息
        self.textEdit.setText('【当前配件信息】\n' +
                              '\t配件组1：' + txt_1 + '、' + txt_2 + '、' + txt_3 + '\n' +
                              '\t配件组2：' + txt_4 + '、' + txt_5 + '、' + txt_6 + '\n' +
                              '【坦克极速前进】\n' +
                              '\t配件组1：缩圈到基础精度所需时间：' + str('{:.3f}'.format(t1)) + 's，' +
                              '缩圈到目标精度所需时间：' + str('{:.3f}'.format(t2)) + 's，' +
                              '最大精度：' + str('{:.3f}'.format(t3)) + 'm\n' +
                              '\t配件组2：缩圈到基础精度所需时间：' + str('{:.3f}'.format(t4)) + 's，' +
                              '缩圈到目标精度所需时间：' + str('{:.3f}'.format(t5)) + 's，' +
                              '最大精度：' + str('{:.3f}'.format(t6)) + 'm\n' +
                              '【坦克全速旋转】旋转角度：' + str(angle) + '°\n' +
                              '\t配件组1：缩圈到基础精度所需总时间：' + str('{:.3f}'.format(t7)) + 's，' +
                              '缩圈到目标精度所需总时间：' + str('{:.3f}'.format(t8)) + 's\n' +
                              '\t配件组2：缩圈到基础精度所需总时间：' + str('{:.3f}'.format(t9)) + 's，' +
                              '缩圈到目标精度所需总时间：' + str('{:.3f}'.format(t10)) + 's\n' +
                              '【坦克开火后】\n' +
                              '\t配件组1：缩圈到基础精度所需时间：' + str('{:.3f}'.format(t11)) + 's，' +
                              '缩圈到目标精度所需时间：' + str('{:.3f}'.format(t12)) + 's\n' +
                              '\t配件组2：缩圈到基础精度所需时间：' + str('{:.3f}'.format(t13)) + 's，' +
                              '缩圈到目标精度所需时间：' + str('{:.3f}'.format(t14)) + 's')
        self.plot_fig()
        return

    # 动作 help 触发
    def help(self):
        QMessageBox.about(self, "帮助", "坦克世界缩圈扩圈计算工具 v1.0\nCopyright 黯流雾雨, 2023")
        return

    def read_file(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel 逗号分隔值文件(*.csv)')
            attr_list = []
            with open(file_name[0], 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    attr_list.append(row)

            # 基础扩圈系数
            self.horizontalSlider_move.setValue(int(float(attr_list[0][0]) * 100))
            self.horizontalSlider_rotate.setValue(int(float(attr_list[1][0]) * 100))
            self.horizontalSlider_gun.setValue(int(float(attr_list[2][0]) * 100))
            self.doubleSpinBox_fire.setValue(round(float(attr_list[3][0]), 2))

            # 瞄准时间和精度
            self.doubleSpinBox_aimTime.setValue(round(float(attr_list[4][0]), 3))
            self.doubleSpinBox_dispersion.setValue(round(float(attr_list[5][0]), 3))
            self.doubleSpinBox_objectDispersion.setValue(round(float(attr_list[6][0]), 3))

            # 极速、旋转速度和装填时间
            self.doubleSpinBox_topSpeed.setValue(round(float(attr_list[7][0]), 1))
            self.doubleSpinBox_hullSpeed.setValue(round(float(attr_list[8][0]), 1))
            self.doubleSpinBox_turretSpeed.setValue(round(float(attr_list[9][0]), 1))
            self.doubleSpinBox_reloadTime.setValue(round(float(attr_list[10][0]), 2))

            # 是否勾选同时旋转车体和旋转角度
            self.radioButton.setChecked(True if attr_list[11][0] == 'True' else False)
            self.spinBox.setValue(int(attr_list[12][0]))

            # 配件选择下拉菜单
            # 第一套配件的选择结果
            self.comboBox_item_1.setCurrentIndex(int(attr_list[13][0]))
            self.comboBox_item_2.setCurrentIndex(int(attr_list[14][0]))
            self.comboBox_item_3.setCurrentIndex(int(attr_list[15][0]))
            self.comboBox_level_1.setCurrentIndex(int(attr_list[16][0]))
            self.comboBox_level_2.setCurrentIndex(int(attr_list[17][0]))
            self.comboBox_level_3.setCurrentIndex(int(attr_list[18][0]))

            # 第二套配件的选择结果
            self.comboBox_item_4.setCurrentIndex(int(attr_list[19][0]))
            self.comboBox_item_5.setCurrentIndex(int(attr_list[20][0]))
            self.comboBox_item_6.setCurrentIndex(int(attr_list[21][0]))
            self.comboBox_level_4.setCurrentIndex(int(attr_list[22][0]))
            self.comboBox_level_5.setCurrentIndex(int(attr_list[23][0]))
            self.comboBox_level_6.setCurrentIndex(int(attr_list[24][0]))

            QMessageBox.about(self, "打开成功", "打开配置属性文件成功，文件名：" + str(file_name[0]))
        except FileNotFoundError:
            QMessageBox.about(self, "打开失败", "打开文件失败，可能是文件不存在或类型错误")

    def save_file(self):
        try:
            file_name = QFileDialog.getSaveFileName(self, '选择文件', 'wot.csv', 'Excel 逗号分隔值文件(*.csv)')

            # 基础扩圈系数
            move_f = self.horizontalSlider_move.value() / 100.0
            rotate_f = self.horizontalSlider_rotate.value() / 100.0
            gun_f = self.horizontalSlider_gun.value() / 100.0
            fire_f = self.doubleSpinBox_fire.value()

            # 瞄准时间和精度
            aim_time = self.doubleSpinBox_aimTime.value()
            dispersion = self.doubleSpinBox_dispersion.value()
            dispersion_obj = self.doubleSpinBox_objectDispersion.value()

            # 极速、旋转速度和装填时间
            top_speed = self.doubleSpinBox_topSpeed.value()
            hull_speed = self.doubleSpinBox_hullSpeed.value()
            turret_speed = self.doubleSpinBox_turretSpeed.value()
            t_reload = self.doubleSpinBox_reloadTime.value()

            # 是否勾选同时旋转车体和旋转角度
            check = self.radioButton.isChecked()
            angle = self.spinBox.value()

            # 配件选择下拉菜单
            # 第一套配件的选择结果
            item_1 = self.comboBox_item_1.currentIndex()
            item_2 = self.comboBox_item_2.currentIndex()
            item_3 = self.comboBox_item_3.currentIndex()
            level_1 = self.comboBox_level_1.currentIndex()
            level_2 = self.comboBox_level_2.currentIndex()
            level_3 = self.comboBox_level_3.currentIndex()

            # 第二套配件的选择结果
            item_4 = self.comboBox_item_4.currentIndex()
            item_5 = self.comboBox_item_5.currentIndex()
            item_6 = self.comboBox_item_6.currentIndex()
            level_4 = self.comboBox_level_4.currentIndex()
            level_5 = self.comboBox_level_5.currentIndex()
            level_6 = self.comboBox_level_6.currentIndex()

            attr_list = [[move_f], [rotate_f], [gun_f], [fire_f], [aim_time], [dispersion], [dispersion_obj],
                         [top_speed], [hull_speed], [turret_speed], [t_reload], [check], [angle],
                         [item_1], [item_2], [item_3], [level_1], [level_2], [level_3],
                         [item_4], [item_5], [item_6], [level_4], [level_5], [level_6]]
            with open(file_name[0], 'w', newline="") as f:
                writer = csv.writer(f)
                for row in range(len(attr_list)):
                    writer.writerow(attr_list[row])

            QMessageBox.about(self, "保存成功", "保存配置属性文件成功，文件名：" + str(file_name[0]))
        except FileNotFoundError:
            QMessageBox.about(self, "保存失败", "保存文件失败")

    def value_change_move(self):
        move_f = self.horizontalSlider_move.value() / 100.0
        self.label_move.setText('车体移动扩圈系数：' + str('{:.2f}'.format(move_f)))
        return

    def value_change_rotate(self):
        rotate_f = self.horizontalSlider_rotate.value() / 100.0
        self.label_rotate.setText('车体旋转扩圈系数：' + str('{:.2f}'.format(rotate_f)))
        return

    def value_change_gun(self):
        gun_f = self.horizontalSlider_gun.value() / 100.0
        self.label_gun.setText('炮塔旋转扩圈系数：' + str('{:.2f}'.format(gun_f)))
        return

    def plot_fig(self):
        # 基础扩圈系数
        move_f = self.horizontalSlider_move.value() / 100.0
        rotate_f = self.horizontalSlider_rotate.value() / 100.0
        gun_f = self.horizontalSlider_gun.value() / 100.0
        fire_f = self.doubleSpinBox_fire.value()

        # 瞄准时间和精度
        aim_time = self.doubleSpinBox_aimTime.value()
        dispersion = self.doubleSpinBox_dispersion.value()
        dispersion_obj = self.doubleSpinBox_objectDispersion.value()

        # 极速、旋转速度和装填时间
        top_speed = self.doubleSpinBox_topSpeed.value()
        hull_speed = self.doubleSpinBox_hullSpeed.value()
        turret_speed = self.doubleSpinBox_turretSpeed.value()
        t_reload = self.doubleSpinBox_reloadTime.value()

        # 是否勾选同时旋转车体和旋转角度
        check = self.radioButton.isChecked()
        angle = self.spinBox.value()

        # 配件选择下拉菜单
        # 第一套配件的选择结果
        item_1 = self.comboBox_item_1.currentIndex()
        item_2 = self.comboBox_item_2.currentIndex()
        item_3 = self.comboBox_item_3.currentIndex()
        level_1 = self.comboBox_level_1.currentIndex()
        level_2 = self.comboBox_level_2.currentIndex()
        level_3 = self.comboBox_level_3.currentIndex()

        # 第二套配件的选择结果
        item_4 = self.comboBox_item_4.currentIndex()
        item_5 = self.comboBox_item_5.currentIndex()
        item_6 = self.comboBox_item_6.currentIndex()
        level_4 = self.comboBox_level_4.currentIndex()
        level_5 = self.comboBox_level_5.currentIndex()
        level_6 = self.comboBox_level_6.currentIndex()

        # 传参给 Matplotlib 画图
        self.canvas.plot_figure(move_f, rotate_f, gun_f, fire_f, aim_time, dispersion, dispersion_obj,
                                top_speed, hull_speed, turret_speed, t_reload, check, angle,
                                item_1, item_2, item_3, level_1, level_2, level_3,
                                item_4, item_5, item_6, level_4, level_5, level_6)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 在 QApplication 方法中初始化，创建应用程序对象
    myWindow = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWindow.show()  # 在桌面显示主窗口 myWindow
    sys.exit(app.exec_())  # 结束进程，退出程序
