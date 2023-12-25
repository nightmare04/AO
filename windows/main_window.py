from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QTableWidgetItem, QTableWidget
from ui import Ui_MainWindow
from modules import Database, ClickQlabel, Check
from datetime import datetime
from windows import EditLK, AddLk, SetupPodr, SetupSpec, SetupType, SetupPlane, Complete, Listlk, Checks


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # myappid = 'mycompany.myproduct.subproduct.version'
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.checks = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.new_form = None
        self.setWindowTitle("Старший инженер по специальности")


        self.checks_layout = QVBoxLayout()
        self.ui.checks_groupbox.setLayout(self.checks_layout)

        self.init_table()
        self.show()

        self.ui.add_btn.clicked.connect(self.add_form)
        self.ui.podr_setup_action.triggered.connect(self.open_setup_podr)
        self.ui.spec_setup_action.triggered.connect(self.open_setup_spec)
        self.ui.types_setup_action.triggered.connect(self.open_setup_type)
        self.ui.plane_setup_action.triggered.connect(self.open_setup_plane)
        self.ui.lk_action.triggered.connect(self.list_lk)
        self.ui.checks_setup_action.triggered.connect(self.open_setup_checks)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
            self.fill_checks()
        return QtWidgets.QWidget.event(self, e)

    def open_setup_checks(self):
        self.new_form = Checks()
        self.new_form.show()

    def fill_checks(self):
        self.checks = []
        for check in Check.select():
            self.checks.append()
        self.clear_layout()

        for ch in self.checks:
            last_check = QDate(datetime.strptime(ch.last_check, '%d.%m.%Y'))
            next_check = self.add_period(last_check, ch.period)
            ost = (next_check.toPyDate() - datetime.date(datetime.today())).days + 1
            label = ClickQlabel(f'Следующая проверка {ch.name_check}: {next_check.toString('dd.MM.yyyy')}, '
                                f'осталось {ost} дней')
            label.check = ch
            label.clicked.connect(self.open_edit_check)
            self.checks_layout.addWidget(label)

    def open_edit_check(self):
        sender = self.sender()
        ch = sender.check
        self.new_form = EditCheck(ch)
        self.new_form.show()

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
        self.new_form.show()

    def open_setup_plane(self):
        self.new_form = SetupPlane(self.db)
        self.new_form.show()

    def open_setup_podr(self):
        self.new_form = SetupPodr(self.db)
        self.new_form.show()

    def open_setup_type(self):
        self.new_form = SetupType(self.db)
        self.new_form.show()

    def open_setup_spec(self):
        self.new_form = SetupSpec(self.db)
        self.new_form.show()

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
        listk = self.db.load_lk(self.ui.tableWidget.item(row, 0).text())
        self.new_form = Complete(listk, self.db)
        self.new_form.show()

    def fill_table(self):
        """Заполняем таблицу долгами"""
        self.lks = self.db.load_all_uncomplete_lk()
        self.ui.tableWidget.setRowCount(len(self.lks))
        row = 0
        for listk in self.lks:
            if not listk.complete:
                btn = QPushButton("Изменить")
                btn.lk = listk
                btn.clicked.connect(self.open_edit_form)
                ost = (datetime.strptime(listk.date_vypoln, '%d.%m.%Y') - datetime.today())
                if ost.days + 1 < 5:
                    ost_wid = QTableWidgetItem(str(ost.days + 1))
                    ost_wid.setBackground(QColor("red"))
                else:
                    ost_wid = QTableWidgetItem(str(ost.days + 1))

                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(listk.id_lk)))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(listk.tlg)))
                self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(listk.date_tlg)))
                self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(listk.date_vypoln)))
                self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(str(listk.lk)))
                self.ui.tableWidget.setItem(row, 5, ost_wid)
                self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(self.calc_nevyp(listk)))
                self.ui.tableWidget.setCellWidget(row, 7, btn)
                row += 1

    def calc_nevyp(self, listk) -> str:
        done, not_done = self.db.get_not_done_planes(listk)
        if len(not_done) == 0:
            return "Выполнено на всех!"
        else:
            text = ''
            for pl in not_done:
                text += f'{pl.bort_num} ,'

            return text[:-2]

    def add_form(self):
        """Открываем новую форму добавления листа контроля"""
        self.new_form = AddLk(self.db)
        self.new_form.show()

    def open_edit_form(self):
        """Открытие формы редактирования листа контроля"""
        sender = self.sender()
        self.new_form = EditLK(sender.lk, self.db)
        self.new_form.show()
