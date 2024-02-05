from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QTableWidgetItem
from ui import Ui_MainWindow
from modules import ClickQlabel, CheckM, ListControlM, CompleteLM, PlaneM
from datetime import datetime
from windows import (Systems, EditLK, AddLk, SetupUnit, SetupSubunit, SetupType, SetupPlane,
                     Complete, Listlk, Checks, EditCheck, Condition)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # myappid = 'mycompany.myproduct.subproduct.version'
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.checks = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.new_form = None
        self.lks = []
        self.setWindowTitle("Старший инженер по АО")

        self.checks_layout = QVBoxLayout()
        self.ui.checks_groupbox.setLayout(self.checks_layout)

        self.init_table()
        self.show()

        self.ui.add_btn.clicked.connect(self.add_form)
        self.ui.podr_setup_action.triggered.connect(self.open_setup_unit)
        self.ui.spec_setup_action.triggered.connect(self.open_setup_subunit)
        self.ui.types_setup_action.triggered.connect(self.open_setup_type)
        self.ui.plane_setup_action.triggered.connect(self.open_setup_plane)
        self.ui.lk_action.triggered.connect(self.list_lk)
        self.ui.checks_setup_action.triggered.connect(self.open_setup_checks)
        self.ui.system_action.triggered.connect(self.open_setup_system)
        self.ui.cond_action.triggered.connect(self.open_conditions)
        self.fill_table()

    # def event(self, e):
    #     if e.type() == QtCore.QEvent.Type.WindowActivate:
    #         self.fill_table()
    #         self.fill_checks()
    #     return QtWidgets.QWidget.event(self, e)

    def open_conditions(self):
        self.new_form = Condition()
        self.new_form.show()

    def open_setup_system(self):
        self.new_form = Systems()
        self.new_form.show()

    def open_setup_checks(self):
        self.new_form = Checks()
        self.new_form.exec()
        self.fill_checks()

    def fill_checks(self):
        self.checks = CheckM.select()
        self.clear_layout()

        for ch in self.checks:
            last_check = QDate(ch.last_check)
            next_check = self.add_period(last_check, ch.period)
            ost = (next_check.toPyDate() - datetime.date(datetime.today())).days + 1
            label = ClickQlabel(f"Следующая проверка {ch.name}:{next_check.toString('dd.MM.yyyy')}"
                                f" осталось {ost} дня/дней")
            label.check = ch
            label.clicked.connect(self.open_edit_check)
            self.checks_layout.addWidget(label)

    # noinspection PyUnresolvedReferences
    def open_edit_check(self):
        sender = self.sender()
        ch = sender.check
        self.new_form = EditCheck(ch)
        self.new_form.exec()
        self.fill_checks()

    def clear_layout(self):
        while self.checks_layout.count():
            item = self.checks_layout.takeAt(0)
            widget = item.widget()
            self.checks_layout.removeWidget(widget)

    @staticmethod
    def add_period(date: QDate, period: 'str') -> QDate:
        if period == 'месяц':
            next_check = date.addMonths(1)
            return next_check

        if period == 'квартал':
            next_check = date.addMonths(3)
            return next_check

        if period == 'год':
            next_check = date.addMonths(12)
            return next_check

    def list_lk(self):
        self.new_form = Listlk(self)
        self.new_form.exec()
        self.fill_table()

    def open_setup_plane(self):
        self.new_form = SetupPlane()
        self.new_form.exec()

    def open_setup_unit(self):
        self.new_form = SetupUnit()
        self.new_form.exec()

    def open_setup_type(self):
        self.new_form = SetupType()
        self.new_form.exec()

    def open_setup_subunit(self):
        self.new_form = SetupSubunit()
        self.new_form.exec()

    def init_table(self):
        """Описываем параметры таблицы долгов"""
        self.ui.tableWidget.setColumnCount(8)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "ID",
            "Телеграмма",
            "Дата ТЛГ",
            "Срок выполнения",
            "Номер ЛК",
            "Осталось дней",
            "Не выполнено",
            ""
        ])
        self.ui.tableWidget.hideColumn(0)
        self.ui.tableWidget.cellDoubleClicked.connect(lambda row: self.open_complete_form(row))
        self.ui.tableWidget.setSortingEnabled(True)

    def open_complete_form(self, row):
        listk = ListControlM.get(ListControlM.id == self.ui.tableWidget.item(row, 0).text())
        self.new_form = Complete(listk)
        self.new_form.exec()
        self.fill_table()

    # noinspection PyUnresolvedReferences
    def fill_table(self):
        """Заполняем таблицу долгами"""
        self.lks = ListControlM.select().where(ListControlM.complete_flag == False)
        self.ui.tableWidget.setRowCount(len(self.lks))
        row = 0
        for listk in self.lks:
            listk: ListControlM
            btn = QPushButton("Изменить")
            btn.lk = listk
            btn.clicked.connect(self.open_edit_form)
            ost = (listk.date_deadline - datetime.today().date())
            if ost.days + 1 < 5:
                ost_wid = QTableWidgetItem(str(ost.days + 1))
                ost_wid.setBackground(QColor("red"))
            else:
                ost_wid = QTableWidgetItem(str(ost.days + 1))

            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(listk.id)))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(listk.telegram)))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(listk.date_telegram.strftime("%d.%m.%Y"))))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(listk.date_deadline.strftime("%d.%m.%Y"))))
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(str(listk.number_lk)))
            self.ui.tableWidget.setItem(row, 5, ost_wid)
            self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(self.calc_nevyp(listk)))
            self.ui.tableWidget.setCellWidget(row, 7, btn)
            row += 1

    @staticmethod
    def calc_nevyp(listk) -> str:
        not_done = []
        for plane_id in listk.planes_for_exec:
            plane = PlaneM.get(PlaneM.id == plane_id)
            if not len(CompleteLM.select().where(
                    CompleteLM.id_plane == plane_id,
                    CompleteLM.id_list == listk.id)) == len(listk.specialties_for_exec):
                not_done.append(plane.tail_number)

        if len(not_done) == 0:
            return "Выполнено на всех!"
        else:
            text = ''
            for pl in not_done:
                text += f'{pl}, '

            return text[:-2]

    def add_form(self):
        """Открываем новую форму добавления листа контроля"""
        self.new_form = AddLk()
        self.new_form.exec()
        self.fill_table()

    # noinspection PyUnresolvedReferences
    def open_edit_form(self):
        """Открытие формы редактирования листа контроля"""
        sender = self.sender()
        self.new_form = EditLK(sender.lk)
        self.new_form.exec()
        self.fill_table()
