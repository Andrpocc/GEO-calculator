# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon
from sympy import Point
import matplotlib.pyplot as plt
import seaborn as sns
from Qtui_for_geotasks import Ui_MainWindow
from geo_tasks import *


def coords(coords_string):
    """Разделение строки координат на X и Y"""
    coords_list = coords_string.split(' ')
    x = float(coords_list[0])
    y = float(coords_list[1])
    return x, y


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon_error = QIcon()  # Инициализация иконки для окна ошибки
        icon_error.addPixmap(QPixmap(":/icons/icons/error.ico"), QIcon.Normal, QIcon.Off)
        self.msg_error = QMessageBox()
        self.msg_error.setText('Введены некорректные данные!')
        self.msg_error.setWindowTitle('Ошибка')
        self.msg_error.setWindowIcon(icon_error)
        self.x_intersection, self.y_intersection = 0, 0
        self.ui.button_ogz.clicked.connect(self.show_page1)  # Соединение кнопок интерфейса с их функциями
        self.ui.button_pgz.clicked.connect(self.show_page2)
        self.ui.button_square.clicked.connect(self.show_page3)
        self.ui.button_intersection.clicked.connect(self.show_page4)
        self.ui.button_clean.clicked.connect(self.log_cleannig)
        self.ui.ogz_button_submit.clicked.connect(self.ogz_submitting)
        self.ui.pgz_button_submit.clicked.connect(self.pgz_submitting)
        self.ui.square_button_submit.clicked.connect(self.square_submitting)
        self.ui.square_button_import.clicked.connect(self.square_import)
        self.ui.intersection_button_submit.clicked.connect(self.intersection_submitting)
        self.ui.intersection_button_plot.clicked.connect(self.show_plot)



    def show_page1(self):
        """Отображение страницы с ОГЗ"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_page2(self):
        """Отображение страницы с ПГЗ"""
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_page3(self):
        """Отображение страницы с площадью"""
        self.ui.stackedWidget.setCurrentIndex(2)

    def show_page4(self):
        """Отображение страницы с точкой пересечения"""
        self.ui.stackedWidget.setCurrentIndex(3)

    def log_cleannig(self):
        self.ui.textEdit.clear()

    def ogz_submitting(self):
        try:
            x1 = float(self.ui.ogz_lineedit_x1.text())
            y1 = float(self.ui.ogz_lineedit_y1.text())
            x2 = float(self.ui.ogz_lineedit_x2.text())
            y2 = float(self.ui.ogz_lineedit_y2.text())
            g, m, c, s = ogz(x1, y1, x2, y2)
            s = round(s, int(self.ui.ogz_spinBox.text()))
            self.ui.ogz_label_answer.setText('α={}°{}\'{}\" S={} м'.format(g, m, c, s))
            self.ui.ogz_label_answer.setAlignment(Qt.AlignCenter)
            self.ui.textEdit.append('Обратная геодезическая задача\nВведенные данные:\
            P1=({},{}) м P2=({},{}) м\nРезультат:\nS={} м α={}°{}\'{}\"\n'.format(x1, y1, x2, y2, s, g, m, c))
        except ValueError:
            self.msg_error.show()

    def pgz_submitting(self):
        try:
            x1 = float(self.ui.pgz_lineedit_x.text())
            y1 = float(self.ui.pgz_lineedit_y.text())
            s = float(self.ui.pgz_lineedit_s.text())
            ug = self.ui.pgz_lineedit_g.text()
            ug_format = ug.replace('°', ' ')
            ug_format = ug_format.replace('\'', ' ')
            ug_format = ug_format.replace('\"', '')
            ug_list = ug_format.split(' ')
            g = float(ug_list[0])
            m = float(ug_list[1])
            c = float(ug_list[2])
            x2, y2 = pgz(x1, y1, g, m, c, s)
            index = int(self.ui.pgz_spinBox.text())
            x2 = round(x2, index)
            y2 = round(y2, index)
            self.ui.pgz_label_answer.setText('X={} м Y={} м'.format(x2, y2))
            self.ui.pgz_label_answer.setAlignment(Qt.AlignCenter)
            self.ui.textEdit.append('Прямая геодезическая задача\nВведенные данные:\
            X={} м Y={} м\nS={} м α={}\nРезультат:\nX={} м Y={} м\n'.format(x1, y1, s, ug, x2, y2))
        except ValueError:
            self.msg_error.show()

    def square_submitting(self):
        try:
            text = self.ui.square_textedit.toPlainText()
            points = text.split('\n')
            for i in range(len(points)):
                points[i] = points[i].split(' ')
            for point in points:
                for i in range(2):
                    point[i] = float(point[i])
            square = polygon_square(points)
            square = round(square, int(self.ui.square_spinBox.text()))
            self.ui.square_label_answer.setText('Площадь={} кв м'.format(square))
            self.ui.square_label_answer.setAlignment(Qt.AlignCenter)
            self.ui.textEdit.append('Площадь полигона\nВведенные данные:\n{}\nРезультат:\nP={} кв м\n'.format(text, square))

        except ValueError:
            self.msg_error.show()

    def square_import(self):
        path = QFileDialog.getOpenFileName(self, self.tr("Импортировать координаты"), filter=self.tr("Text files (*.txt)"))
        if len(path[0]) != 0:
            with open(path[0], 'r') as data:
                points = data.read()
            self.ui.square_textedit.clear()
            self.ui.square_textedit.append(points)

    def intersection_submitting(self):
        try:
            x1, y1 = coords(self.ui.intersection_lineedit_p1.text())
            p1 = Point(x1, y1)
            x2, y2 = coords(self.ui.intersection_lineedit_p2.text())
            p2 = Point(x2, y2)
            x3, y3 = coords(self.ui.intersection_lineedit_p3.text())
            p3 = Point(x3, y3)
            x4, y4 = coords(self.ui.intersection_lineedit_p4.text())
            p4 = Point(x4, y4)
            self.y_intersection, self.x_intersection = intersection_of_segments(p1, p2, p3, p4)
            self.ui.textEdit.append('Точка пересечения\nВведенные данные:\nP1=({}, {}) м P2=({}, {}) м\
                            P3=({}, {}) м P4=({}, {}) м\nРезультат:'.format(x1, y1, x2, y2, x3, y3, x4, y4))
            if self.x_intersection == 0 and self.y_intersection == 0:
                self.ui.intersection_label_answer.setText('Нет точки пересечения!')
                self.ui.intersection_label_answer.setAlignment(Qt.AlignCenter)
                self.ui.textEdit.append('Нет точки пересечения!\n')
            else:
                x_intersection = round(self.x_intersection, int(self.ui.intersection_spinBox.text()))
                y_intersection = round(self.y_intersection, int(self.ui.intersection_spinBox.text()))
                self.ui.intersection_label_answer.setText('X={} м Y={} м'.format(x_intersection, y_intersection))
                self.ui.intersection_label_answer.setAlignment(Qt.AlignCenter)
                self.ui.textEdit.append('P=({}, {}) м\n'.format(x_intersection, y_intersection))
        except ValueError:
            self.msg_error.show()

    def show_plot(self):
        try:
            sns.set(style='whitegrid')
            x1, y1 = coords(self.ui.intersection_lineedit_p1.text())
            x2, y2 = coords(self.ui.intersection_lineedit_p2.text())
            x3, y3 = coords(self.ui.intersection_lineedit_p3.text())
            x4, y4 = coords(self.ui.intersection_lineedit_p4.text())
            x1_list = [x1, x2]
            y1_list = [y1, y2]
            x2_list = [x3, x4]
            y2_list = [y3, y4]
            plt.figure('Точка пересечение')
            plt.xlabel('Ось Y')
            plt.ylabel('Ось X')
            plt.plot(y1_list, x1_list, label='P1-P2', zorder=1)
            plt.plot(y2_list, x2_list, zorder=1, label='P3-P4')
            plt.legend()
            if self.x_intersection and self.y_intersection != 0:
                plt.scatter(self.y_intersection, self.x_intersection, color='green', zorder=2)
            plt.show()
        except ValueError:
            self.msg_error.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
