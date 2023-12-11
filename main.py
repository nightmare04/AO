from PyQt6.QtWidgets import (QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QGroupBox,
                             QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox,
                             QDateEdit, QWidgetAction, QLayoutItem)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor
from ui import *
from modules import *
from datetime import datetime
from collections import namedtuple
from docxtpl import DocxTemplate
import json
import os
import ctypes


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        db.create_connection()
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.new_form = None
        self.lks = []
        self.setWindowTitle("Старший инженер по специальности")

        self.checks = []

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
        self.checks = db.load_all_checks()
        self.clear_layout()

        for ch in self.checks:
            last_check = QDate(datetime.strptime(ch.last_check, '%d.%m.%Y'))
            next_check = self.add_period(last_check, ch.period)
            ost = (next_check.toPyDate() - datetime.date(datetime.today())).days + 1
            label = ClickQlabel(f'Следующая проверка {ch.name_check}: {next_check.toString('dd.MM.yyyy')}, осталось {ost} дней')
            label.check = ch
            label.clicked.connect(self.open_edit_check)
            self.checks_layout.addWidget(label)

    def open_edit_check(self):
        sender = self.sender()
        check = sender.check
        self.new_form = EditCheck(check)
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
        self.new_form = Listlk()
        self.new_form.show()

    def open_setup_plane(self):
        self.new_form = SetupPlane()
        self.new_form.show()

    def open_setup_podr(self):
        self.new_form = SetupPodr()
        self.new_form.show()

    def open_setup_type(self):
        self.new_form = SetupType()
        self.new_form.show()

    def open_setup_spec(self):
        self.new_form = SetupSpec()
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
        listk = db.load_lk(self.ui.tableWidget.item(row, 0).text())
        self.new_form = Complete(listk)
        self.new_form.show()

    def fill_table(self):
        """Заполняем таблицу долгами"""
        self.lks = db.load_all_uncomplete_lk()
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

    @staticmethod
    def calc_nevyp(listk) -> str:
        done, not_done = db.get_not_done_planes(listk)
        if len(not_done) == 0:
            return "Выполнено на всех!"
        else:
            text = ''
            for pl in not_done:
                text += f'{pl.bort_num} ,'

            return text[:-2]

    def add_form(self):
        """Открываем новую форму добавления листа контроля"""
        self.new_form = AddLk()
        self.new_form.show()

    def open_edit_form(self):
        """Открытие формы редактирования листа контроля"""
        sender = self.sender()
        self.new_form = EditLK(sender.lk)
        self.new_form.show()


class AddLk(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lk = LK()
        self.spec_btns = []
        self.type_btns = []
        self.podr_btns = []
        self.plane_btns = []
        self.plane_groups = []

        self.ui = Ui_Add_lk_form()
        self.ui.setupUi(self)
        self.ui.TlgDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.SrokDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.add_btn.clicked.connect(self.add_lk_to_db)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.fill_planes()
        self.fill_planes_to_podr()
        self.init_spec()
        self.setAcceptDrops(True)
        self.fill_selectors()

    def fill_selectors(self):
        main_groupbox = QGroupBox("Выбрать:")
        group_layout = QHBoxLayout()
        main_groupbox.setLayout(group_layout)
        self.ui.selectorLayout.addWidget(main_groupbox)

        podr_groupbox = QGroupBox("по подразделению:")
        group_layout.addWidget(podr_groupbox)
        podr_groupbox_layout = QGridLayout()
        podr_groupbox.setLayout(podr_groupbox_layout)
        podrs = db.load_all_podr()

        row = 0
        col = 0
        for pd in podrs:
            btn = QPushButton(pd.name_podr)
            btn.setCheckable(True)
            btn.clicked.connect(self.select_by_podr)
            btn.podr = pd
            self.podr_btns.append(btn)
            if btn.podr.with_planes:
                if col < 4:
                    podr_groupbox_layout.addWidget(btn, row, col)
                    col += 1
                else:
                    col = 0
                    row += 1
                    podr_groupbox_layout.addWidget(btn, row, col)
                    col += 1

        type_groupbox = QGroupBox("по типу:")
        group_layout.addWidget(type_groupbox)
        type_groupbox_layout = QGridLayout()
        type_groupbox.setLayout(type_groupbox_layout)
        types = db.load_all_type()

        row = 0
        col = 0
        for tp in types:
            btn = QPushButton(tp.name_type)
            btn.setCheckable(True)
            btn.clicked.connect(self.select_by_type)
            btn.type = tp
            self.type_btns.append(btn)
            if col < 4:
                type_groupbox_layout.addWidget(btn, row, col)
                col += 1
            else:
                col = 0
                row += 1
                type_groupbox_layout.addWidget(btn, row, col)
                col += 1

    def select_by_podr(self):

        for btn in self.type_btns:
            btn.setChecked(False)

        btns = self.findChildren(DragButton)
        for podr_btn in self.podr_btns:
            for btn in btns:
                if btn.plane.id_podr == podr_btn.podr.id_podr and podr_btn.isChecked():
                    btn.setChecked(True)
                elif btn.plane.id_podr == podr_btn.podr.id_podr:
                    btn.setChecked(False)

    def select_by_type(self):
        for btn in self.podr_btns:
            btn.setChecked(False)

        btns = self.findChildren(DragButton)
        for type_btn in self.type_btns:
            for btn in btns:
                if btn.plane.id_type == type_btn.type.id_type and type_btn.isChecked():
                    btn.setChecked(True)
                elif btn.plane.id_type == type_btn.type.id_type:
                    btn.setChecked(False)

    def fill_planes(self):
        for pl in db.load_all_planes():
            btn = DragButton(text=str(pl.bort_num))
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = pl
            self.plane_btns.append(btn)

    def fill_planes_to_podr(self):
        all_podr = db.load_all_podr()
        for p in all_podr:
            row = 0
            col = 0
            groupbox = DragGroupbox(p.name_podr)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.podr = p
            groupbox.plane_btns = []
            self.ui.planesLayout.addWidget(groupbox)
            self.plane_groups.append(groupbox)
            for plane_btn in self.plane_btns:
                if plane_btn.plane.id_podr == p.id_podr:
                    if col < 3:
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        row += 1
                        col = 0
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1

    def update_planes(self):
        for groupbox in self.plane_groups:
            layout = QGridLayout()
            groupbox.setLayout(layout)
            col = 0
            row = 0
            for plane_btn in self.plane_btns:
                if plane_btn.plane.id_podr == groupbox.podr.id_podr:
                    if col < 3:
                        groupbox.layout().addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        col = 0
                        row += 1
                        groupbox.layout().addWidget(plane_btn, row, col)
                        col += 1
        for btn in self.type_btns:
            if btn.isChecked():
                self.select_by_type()

        for btn in self.podr_btns:
            if btn.isChecked():
                self.select_by_podr()

    def check_toggle(self):
        """Проверка флага на подразделении"""
        sender = self.sender()
        for btn in sender.plane_btns:
            if sender.isChecked():
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def init_spec(self):
        """Готовим специальности"""
        all_spec = db.load_all_spec()
        groupbox = QGroupBox("Специальности")
        layout_spec = QHBoxLayout()
        groupbox.setLayout(layout_spec)
        self.ui.SpecLayout.addWidget(groupbox)
        for s in all_spec:
            btn = QPushButton(s.name_spec)
            btn.setCheckable(True)
            btn.spec = s
            self.spec_btns.append(btn)
            layout_spec.addWidget(btn)

    def add_lk_to_db(self):
        """Добавляем лист контроля в базу данных"""
        data = LK()
        data.pack_lk(self)
        db.add_lk(data)
        self.close()


class EditLK(AddLk):
    def __init__(self, listk):
        super().__init__()
        self.edit = True
        self.lk = listk
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle(f"Лист контроля №{self.lk.lk}")
        self.ui.add_btn.setText("Сохранить")
        self.ui.add_btn.clicked.disconnect()
        self.ui.add_btn.clicked.connect(self.save_lk)
        self.ui.cancel_btn.setText("Удалить")
        self.ui.cancel_btn.clicked.disconnect()
        self.ui.cancel_btn.clicked.connect(self.delete_lk)
        self.load_lk()
        self.fill_planes()
        self.update_planes()

    def fill_planes(self):
        for id_plane, id_podr in self.lk.planes.items():
            p = db.load_plane(id_plane)
            p.id_podr = id_podr
            btn = DragButton(text=str(p.bort_num))
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = p
            self.plane_btns.append(btn)

        for btn in self.plane_btns:
            if btn.plane.id_plane in self.lk.komu_planes:
                btn.setChecked(True)

    def load_lk(self):
        """Подгружаем лист контроля"""
        self.ui.TlgLineEdit.setText(self.lk.tlg)
        self.ui.TlgDateEdit.setDate(datetime.strptime(str(self.lk.date_tlg), '%d.%m.%Y'))
        self.ui.SrokDateEdit.setDate(datetime.strptime(str(self.lk.date_vypoln), '%d.%m.%Y'))
        self.ui.textEdit.setText(self.lk.opisanie)
        self.ui.LkLineEdit.setText(self.lk.lk)

        for plane_btn in self.plane_btns:
            plane_btn.setChecked(False)
            if plane_btn.plane.id_plane in self.lk.komu_planes:
                plane_btn.setChecked(True)

        for spec_btn in self.spec_btns:
            spec_btn.setChecked(False)
            if spec_btn.spec.id_spec in self.lk.komu_spec:
                spec_btn.setChecked(True)

    def save_lk(self):
        listk = LK()
        listk.pack_lk(self)
        db.update_lk(listk)
        self.close()

    def delete_lk(self):
        db.delete_lk(self.lk)
        self.close()


class Complete(QtWidgets.QWidget):
    def __init__(self, listk):
        super().__init__()
        self.plane_complete = None
        self.lk = listk
        self.podrs = []
        self.plane_btns = []
        self.plane_groups = []
        self.ui = Ui_CompleteForm()
        self.ui.setupUi(self)

        self.ui.create_doc_btn.clicked.connect(self.create_doc)
        self.ui.save_btn.clicked.connect(self.save_lk)

        self.ui.otvet_dateedit.setDate(QtCore.QDate().currentDate())
        self.setWindowTitle(f"Лист контроля №{str(self.lk.lk)}")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.init_planes()

    def init_planes(self):
        for id_plane, id_podr in self.lk.planes.items():
            pl = db.load_plane(id_plane)
            pl.id_podr = id_podr
            btn = QPushButton(str(pl.bort_num))
            btn.setFixedWidth(40)
            btn.plane = pl
            btn.clicked.connect(self.open_plane_complete)
            btn.setChecked(True)
            self.plane_btns.append(btn)

        all_podr = db.load_all_podr()
        for p in all_podr:
            groupbox = QGroupBox(p.name_podr)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.podr = p
            groupbox.plane_btns = []

            row = 0
            col = 0
            for plane_btn in self.plane_btns:
                if (plane_btn.plane.id_plane in self.lk.komu_planes) and (plane_btn.plane.id_podr == p.id_podr):
                    if col < 3:
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        row += 1
                        col = 0
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1

                self.ui.podr_layout.addWidget(groupbox)
                self.plane_groups.append(groupbox)

        self.ui.complete_checkbox.setChecked(bool(self.lk.complete))
        self.ui.otvet_linedit.setText(self.lk.otvet)
        if not self.lk.date_otvet == '':
            self.ui.otvet_dateedit.setDate(datetime.strptime(str(self.lk.date_otvet), '%d.%m.%Y'))

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.check_complete()
        return QtWidgets.QWidget.event(self, e)

    def check_complete(self):
        for btn in self.plane_btns:
            if len(db.get_complete(self.lk, btn.plane)) == len(self.lk.komu_spec):
                btn.setStyleSheet("background-color: green; color: white;")

            else:
                btn.setStyleSheet("background-color: red; color: white;")

    def create_doc(self):
        context = {
            'tlg': str(self.lk.tlg),
            'date_tlg': str(self.lk.date_tlg),
            'lk': str(self.lk.lk),
            'today': datetime.today().strftime("%d.%m.%Y")
        }

        doc = DocxTemplate("templates/Телеграмма.docx")
        doc.render(context)
        doc.save("templates/out.docx")
        os.system("start templates/out.docx")
        self.close()

    def save_lk(self):
        if self.ui.complete_checkbox.isChecked():
            self.lk.complete = 1
        if not self.ui.otvet_linedit.text() == "":
            self.lk.otvet = self.ui.otvet_linedit.text()
            self.lk.date_otvet = self.ui.otvet_dateedit.date().toString('dd.MM.yyyy')
        db.update_lk(self.lk)
        self.close()

    def open_plane_complete(self):
        sender = self.sender()
        self.plane_complete = EditComplete(sender.plane, self.lk)
        self.plane_complete.show()


class EditComplete(QtWidgets.QWidget):
    def __init__(self, pl, listk, parent=None):
        super().__init__(parent)
        self.compl = db.get_complete(listk, pl)
        self.lk = listk
        self.plane = pl
        self.resize(250, 200)
        self.setWindowTitle(f'Самолет №{self.plane.bort_num}')
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.specs = db.load_all_spec()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        for sp in self.specs:
            btn = QPushButton(sp.name_spec)
            btn.spec = sp
            btn.setCheckable(True)
            btn.lk = self.lk
            btn.clicked.connect(self.handle_spec)
            if btn.spec.id_spec in btn.lk.komu_spec:
                self.main_layout.addWidget(btn)
                if int(btn.spec.id_spec) in self.compl:
                    btn.setChecked(True)

    def handle_spec(self):
        sender = self.sender()
        if sender.isChecked():
            db.add_complete(self.lk, self.plane, sender.spec)
        else:
            db.del_complete(self.lk, self.plane, sender.spec)


class SetupPodr(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(240, 400)
        self.add_form = None
        self.change_form = None
        self.setWindowTitle("Подразделения")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QtWidgets.QTableWidget()
        self.init_table()
        self.fill_table()
        self.main_layout.addWidget(self.table)
        self.btns_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.btns_layout)
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.open_add_podr)
        self.close_btn = QtWidgets.QPushButton('Закрыть')
        self.close_btn.clicked.connect(self.close)
        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.close_btn)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def init_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(('id', 'Название', ''))
        self.table.hideColumn(0)

    def fill_table(self):
        podrs = db.load_all_podr()
        self.table.setRowCount(len(podrs))
        row = 0
        for p in podrs:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_podr)
            btn.podr = p
            self.table.setItem(row, 1, QTableWidgetItem(p.name_podr))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_podr(self):
        self.add_form = AddPodr()
        self.add_form.show()

    def open_change_podr(self):
        sender = self.sender()
        self.change_form = EditPodr(sender.podr)
        self.change_form.show()


class AddPodr(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.podr = Podr()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить подразделение')
        self.resize(300, 100)

        self.label = QLabel('Введите имя:')
        self.name_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)

        self.planes_label = QLabel("выполняет работы?:")
        self.with_planes = QCheckBox('')
        self.main_layout.addWidget(self.planes_label, 1, 0)
        self.main_layout.addWidget(self.with_planes, 1, 1)

        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_podr)
        self.main_layout.addWidget(self.add_btn, 2, 0, 1, 2)

    def add_podr(self):
        self.podr.pack_podr(self)
        db.add_podr(self.podr)
        self.close()


class EditPodr(AddPodr):
    def __init__(self, p):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.podr = p
        self.setWindowTitle('Изменить подразделение')
        self.add_btn.setText('Сохранить')

        self.label.setText('Введите новое имя:')
        self.name_edit.setText(p.name_podr)

        self.with_planes.setChecked(bool(self.podr.with_planes))

        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_podr)

        self.del_btn = QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_podr)
        self.main_layout.addWidget(self.del_btn, 4, 0, 1, 2)

    def save_podr(self):
        self.podr.pack_podr(self)
        db.update_podr(self.podr)
        self.close()

    def del_podr(self):
        db.delete_podr(self.podr.id_podr)
        self.close()


class SetupSpec(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.add_form = None
        self.change_form = None
        self.setWindowTitle("Специальности")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QtWidgets.QTableWidget()
        self.init_table()
        self.fill_table()
        self.main_layout.addWidget(self.table)
        self.btns_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.btns_layout)
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.open_add_spec)
        self.close_btn = QtWidgets.QPushButton('Закрыть')
        self.close_btn.clicked.connect(self.close)
        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.close_btn)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def init_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(('id', 'Название', ''))
        self.table.hideColumn(0)

    def fill_table(self):
        specs = db.load_all_spec()
        self.table.setRowCount(len(specs))
        row = 0
        for s in specs:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_spec)
            btn.spec = s
            self.table.setItem(row, 1, QTableWidgetItem(str(s.name_spec)))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_spec(self):
        self.add_form = AddSpec()
        self.add_form.show()

    def open_change_spec(self):
        sender = self.sender()
        self.change_form = EditSpec(sender.spec)
        self.change_form.show()


class AddSpec(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.spec = Spec()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить специальность')
        self.resize(300, 100)

        self.label = QLabel('Введите имя:')
        self.name_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)

        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_spec)
        self.main_layout.addWidget(self.add_btn, 1, 0, 1, 2)

    def add_spec(self):
        self.spec.pack_spec(self)
        db.add_spec(self.spec)
        self.close()


class EditSpec(AddSpec):
    def __init__(self, s):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Изменить специальность')
        self.add_btn.setText('Сохранить')
        self.spec = s
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(str(s.name_spec))
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_spec)
        self.del_btn = QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_spec)
        self.main_layout.addWidget(self.del_btn, 2, 0, 1, 2)

    def save_spec(self):
        self.spec.pack_spec(self)
        db.update_spec(self.spec)
        self.close()

    def del_spec(self):
        db.delete_spec(self.spec.id_spec)
        self.close()


class SetupType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.add_form = None
        self.change_form = None
        self.setWindowTitle("Типы самолетов")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QtWidgets.QTableWidget()
        self.init_table()
        self.fill_table()
        self.main_layout.addWidget(self.table)
        self.btns_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.btns_layout)
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.open_add_type)
        self.close_btn = QtWidgets.QPushButton('Закрыть')
        self.close_btn.clicked.connect(self.close)
        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.close_btn)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def init_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(('id', 'Название', ''))
        self.table.hideColumn(0)

    def fill_table(self):
        types = db.load_all_type()
        self.table.setRowCount(len(types))
        row = 0
        for t in types:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_type)
            btn.type = t
            self.table.setItem(row, 1, QTableWidgetItem(str(t.name_type)))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_type(self):
        self.add_form = AddType()
        self.add_form.show()

    def open_change_type(self):
        sender = self.sender()
        self.change_form = EditType(sender.type)
        self.change_form.show()


class AddType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.type = Type()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить тип самолета')
        self.resize(300, 100)
        self.label = QLabel('Введите тип:')
        self.name_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)
        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_type)
        self.main_layout.addWidget(self.add_btn, 1, 0, 1, 2)

    def add_type(self):
        self.type.pack_type(self)
        db.add_type(self.type)
        self.close()


class EditType(AddType):
    def __init__(self, t):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Изменить тип самолета')
        self.add_btn.setText('Сохранить')
        self.type = t
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(str(self.type.name_type))
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_type)
        self.del_btn = QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_type)
        self.main_layout.addWidget(self.del_btn, 2, 0, 1, 2)

    def save_type(self):
        self.type.pack_type(self)
        db.update_type(self.type)
        self.close()

    def del_type(self):
        db.delete_type(self.type.id_type)
        self.close()


class SetupPlane(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(500, 500)
        self.add_form = None
        self.change_form = None
        self.setWindowTitle("Самолеты")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QtWidgets.QTableWidget()
        self.init_table()
        self.fill_table()
        self.main_layout.addWidget(self.table)
        self.btns_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.btns_layout)
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.open_add_plane)
        self.close_btn = QtWidgets.QPushButton('Закрыть')
        self.close_btn.clicked.connect(self.close)
        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.close_btn)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def init_table(self):
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Тип', 'Бортовой номер', 'Заводской номер', ''))

    def fill_table(self):
        planes = db.load_all_planes_table()
        self.table.setRowCount(len(planes))
        row = 0
        for p in planes:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_plane)
            btn.plane = p
            self.table.setItem(row, 0, QTableWidgetItem(str(p.value(1))))
            self.table.setItem(row, 1, QTableWidgetItem(str(p.value(2))))
            self.table.setItem(row, 2, QTableWidgetItem(str(p.value(3))))
            self.table.setCellWidget(row, 3, btn)

            row += 1

    def open_add_plane(self):
        self.add_form = AddPlane()
        self.add_form.show()

    def open_change_plane(self):
        sender = self.sender()
        self.change_form = EditPlane(sender.plane)
        self.change_form.show()


class AddPlane(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.plane = Plane()
        self.types = {}
        self.podrs = {}
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить самолет')
        self.resize(300, 100)

        self.label = QLabel('Выберите тип:')
        self.type_select = QComboBox()
        self.add_types_combo()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.type_select, 0, 1)

        self.label = QLabel('Выберите подразделение:')
        self.podr_select = QComboBox()
        self.add_podr_combo()
        self.main_layout.addWidget(self.label, 1, 0)
        self.main_layout.addWidget(self.podr_select, 1, 1)

        self.label = QLabel('Бортовой номер:')
        self.bort_num_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 2, 0)
        self.main_layout.addWidget(self.bort_num_edit, 2, 1)

        self.label = QLabel('Заводской номер:')
        self.zav_num_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 3, 0)
        self.main_layout.addWidget(self.zav_num_edit, 3, 1)

        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_plane)
        self.main_layout.addWidget(self.add_btn, 4, 0, 1, 2)

    def add_podr_combo(self):
        podrs = db.load_all_podr()
        res_podr = []
        for p in podrs:
            self.podrs[p.name_podr] = p.id_podr
            res_podr.append(p.name_podr)
        self.podr_select.addItems(res_podr)

    def add_types_combo(self):
        types = db.load_all_type()
        res_type = []
        for t in types:
            self.types[t.name_type] = t.id_type
            res_type.append(t.name_type)
        self.type_select.addItems(res_type)

    def add_plane(self):
        self.plane.pack_plane(self)
        db.add_plane(self.plane)
        self.close()


class EditPlane(AddPlane):
    def __init__(self, p):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.plane = p
        self.setWindowTitle('Изменить самолет')

        self.add_btn.setText('Сохранить')
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_plane)

        self.del_btn = QPushButton('Удалить')
        self.del_btn.clicked.connect(self.del_plane)
        self.main_layout.addWidget(self.del_btn, 5, 0, 1, 2)

        self.fill_plane()

    def fill_plane(self):
        self.bort_num_edit.setText(str(self.plane.bort_num))
        self.zav_num_edit.setText(str(self.plane.zav_num))
        # self.type_select.setCurrentIndex(self.type_select.findText(db.load_type_by_id(self.plane.id_type)))

    def save_plane(self):
        self.plane.pack_plane(self)
        db.update_plane(self.type)
        self.close()

    def del_plane(self):
        db.delete_type(self.type.id_type)
        self.close()


class Listlk(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 400)
        self.setWindowTitle('Листы контроля')
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.table = QTableWidget()
        self.main_layout.addWidget(self.table)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Телеграмма",
            "Дата телеграммы",
            "Срок выполнения",
            "Лист контроля",
            "Ответ",
            "Дата ответа",
            "Выполнено",
            ""
        ])

        self.lks = db.load_all_lk()
        self.fill_table()

    def fill_table(self):
        self.table.setRowCount(len(self.lks))
        row = 0
        for listk in self.lks:
            btn = QPushButton("Изменить")
            btn.lk = listk
            btn.clicked.connect(main.open_edit_form)

            if listk.complete:
                complete = "Выполнено"
            else:
                complete = "Не выполнено"

            self.table.setItem(row, 0, QTableWidgetItem(str(listk.tlg)))
            self.table.setItem(row, 1, QTableWidgetItem(str(listk.date_tlg)))
            self.table.setItem(row, 2, QTableWidgetItem(str(listk.date_vypoln)))
            self.table.setItem(row, 3, QTableWidgetItem(str(listk.lk)))
            self.table.setItem(row, 4, QTableWidgetItem(str(listk.otvet)))
            self.table.setItem(row, 5, QTableWidgetItem(str(listk.date_otvet)))
            self.table.setItem(row, 6, QTableWidgetItem(complete))
            self.table.setCellWidget(row, 7, btn)
            row += 1


class Checks(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 300)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Проверки")
        self.new_window = None

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.table = QTableWidget()
        self.main_layout.addWidget(self.table)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Название', 'Периодичность', 'Дата последней проверки', ''))
        self.table.setColumnWidth(2, 160)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.open_add_form)
        self.main_layout.addWidget(self.add_btn)

        self.all_checks = []
        self.fill_table()

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowUnblocked:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def open_add_form(self):
        self.new_window = AddCheck()
        self.new_window.show()

    def fill_table(self):
        self.all_checks = db.load_all_checks()
        self.table.setRowCount(len(self.all_checks))

        row = 0
        for ch in self.all_checks:
            btn = QPushButton("Изменить")
            btn.check = ch
            btn.clicked.connect(self.edit_check)
            self.table.setItem(row, 0, QTableWidgetItem(ch.name_check))
            self.table.setItem(row, 1, QTableWidgetItem(ch.period))
            self.table.setItem(row, 2, QTableWidgetItem(ch.last_check))
            self.table.setCellWidget(row, 3, btn)

            row += 1

    def edit_check(self):
        btn = self.sender()
        self.new_window = EditCheck(btn.check)
        self.new_window.show()


class AddCheck(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 300)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Добавить проверку")
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.check = Check()

        self.name_label = QLabel("Название:")
        self.name_line_edit = QLineEdit()
        self.main_layout.addWidget(self.name_label, 0, 0)
        self.main_layout.addWidget(self.name_line_edit, 0, 1)

        self.period_label = QLabel("Периодичность:")
        self.period_combobox = QComboBox()
        self.period_combobox.addItems(('месяц', 'квартал', 'год'))
        self.main_layout.addWidget(self.period_label, 1, 0)
        self.main_layout.addWidget(self.period_combobox, 1, 1)

        self.last_check_label = QLabel("Дата проверки:")
        self.last_check_date = QDateEdit()
        self.last_check_date.setCalendarPopup(True)
        self.last_check_date.setDate(QDate.currentDate())
        self.main_layout.addWidget(self.last_check_label, 2, 0)
        self.main_layout.addWidget(self.last_check_date, 2, 1)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_check)
        self.cancel_btn = QPushButton("Закрыть")
        self.cancel_btn.clicked.connect(self.close)
        self.main_layout.addWidget(self.save_btn, 3, 0)
        self.main_layout.addWidget(self.cancel_btn, 3, 1)

    def save_check(self):
        self.check.pack_check(self)
        db.add_check(self.check)
        self.close()


class EditCheck(AddCheck):
    def __init__(self, ch):
        super().__init__()
        self.check = ch
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Изменить проверку")
        self.name_line_edit.setText(ch.name_check)
        self.period_combobox.setCurrentText(ch.period)
        self.save_btn.clicked.disconnect()
        self.save_btn.clicked.connect(self.save_check)
        self.cancel_btn.setText('Удалить')
        self.cancel_btn.clicked.disconnect()
        self.cancel_btn.clicked.connect(self.delete_check)
        self.last_check_date.setDate(datetime.strptime(ch.last_check, '%d.%m.%Y'))

    def save_check(self):
        self.check.pack_check(self)
        db.update_check(self.check)
        self.close()

    def delete_check(self):
        db.delete_check(self.check)
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys

    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    db = Database()
    main = MainWindow()
    sys.exit(app.exec())
