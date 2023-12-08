from PyQt6.QtWidgets import QGridLayout, QTableWidgetItem, QPushButton, QGroupBox, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import QDate
from ui import *
from modules import *
import ctypes
from datetime import datetime


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.add_lk_form = None
        self.edit_form = None
        self.lks = []
        self.init_table()
        self.fill_table()
        self.ui.add_btn.clicked.connect(self.add_form)
        self.setWindowTitle("Старший инженер по специальности")
        self.show()
        db.create_connection()
        self.ui.podr_setup_action.triggered.connect(self.open_setup_podr)
        self.ui.spec_setup_action.triggered.connect(self.open_setup_spec)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def open_setup_podr(self):
        self.setup_window = SetupPodr()
        self.setup_window.show()

    def open_setup_spec(self):
        self.setup_window = SetupSpec()
        self.setup_window.show()

    def init_table(self):
        """Описываем параметры таблицы долгов"""
        self.ui.tableWidget.setColumnCount(len(LK().__dict__)+2)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "ID",
            "Телеграмма",
            "Дата ТЛГ",
            "Срок выполнения",
            "Описание",
            "Номер ЛК",
            "Ответ",
            "Дата ответа",
            "На каких самолетах",
            "Специальности",
            "Выполнено",
            "Осталось дней",
            ""
        ])
        self.ui.tableWidget.hideColumn(0)
        self.ui.tableWidget.hideColumn(4)
        self.ui.tableWidget.hideColumn(6)
        self.ui.tableWidget.hideColumn(7)
        self.ui.tableWidget.hideColumn(8)
        self.ui.tableWidget.hideColumn(9)
        self.ui.tableWidget.hideColumn(10)

    def fill_table(self):
        """Заполняем таблицу долгами"""
        self.lks = db.load_all_lk()
        self.ui.tableWidget.setRowCount(len(self.lks))
        row = 0
        for listkontr in self.lks:
            btn = QPushButton("Изменить")
            btn.lk = listkontr
            btn.clicked.connect(self.open_edit_form)
            ost = (datetime.strptime(listkontr.date_vypoln, '%d.%m.%Y') - datetime.today())
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(listkontr.id_lk)))
            self.ui.tableWidget.setCellWidget(row, 12, btn)
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(listkontr.tlg)))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(listkontr.date_tlg)))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(listkontr.date_vypoln)))
            self.ui.tableWidget.setItem(row, 11, QTableWidgetItem(str(ost.days + 1)))
            row += 1

    def add_form(self):
        """Открываем новую форму добавления листа контроля"""
        self.add_lk_form = AddLk()
        self.add_lk_form.show()

    def open_edit_form(self):
        """Открытие формы редактирования листа контроля"""
        sender = self.sender()
        self.edit_form = EditLK(sender.lk)
        self.edit_form.show()


class AddLk(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lk = LK()
        self.spec_btns = []
        self.plane_btns = []
        self.plane_groups = []
        self.ui = Ui_Add_lk_form()
        self.ui.setupUi(self)
        self.ui.TlgDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.SrokDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.add_btn.clicked.connect(self.add_lk_to_db)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.fill_planes()
        self.init_planes()
        self.init_spec()
        self.setAcceptDrops(True)

    def fill_planes(self):
        for plane in db.load_all_planes():
            btn = DragButton(text=str(plane.bort_num))
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = plane
            btn.setChecked(True)
            self.plane_btns.append(btn)

    def init_planes(self):
        all_podr = db.load_all_podr()
        for podr in all_podr:
            row = 0
            col = 0
            groupbox = DragGroupbox(podr.name_podr)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.setCheckable(True)
            groupbox.podr = podr
            groupbox.plane_btns = []
            groupbox.toggled.connect(self.check_toggle)
            self.ui.planesLayout.addWidget(groupbox)
            self.plane_groups.append(groupbox)
            for plane_btn in self.plane_btns:
                if plane_btn.plane.id_podr == podr.id_podr:
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
        db.add_lk_to_db(data)
        self.close()


class EditLK(AddLk):
    def __init__(self, listkontr):
        super().__init__()
        self.lk = listkontr
        self.setWindowTitle("Изменить")
        self.ui.add_btn.setText("Сохранить")
        self.ui.add_btn.clicked.disconnect()
        self.ui.add_btn.clicked.connect(self.save_lk)
        self.ui.cancel_btn.setText("Удалить")
        self.ui.cancel_btn.clicked.disconnect()
        self.ui.cancel_btn.clicked.connect(self.delete_lk)
        self.load_lk()

    def load_lk(self):
        """Подгружаем лист контроля"""
        self.ui.TlgLineEdit.setText(self.lk.tlg)
        self.ui.TlgDateEdit.setDate(datetime.strptime(self.lk.date_tlg, '%d.%m.%Y'))
        self.ui.SrokDateEdit.setDate(datetime.strptime(self.lk.date_vypoln, '%d.%m.%Y'))
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
        data = LK()
        data.pack_lk(self)
        db.update_lk_in_db(data)
        self.close()

    def delete_lk(self):
        db.delete_lk(self.lk)
        self.close()


class SetupPodr(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.close_btn)

    def init_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(('id', 'Название', ''))
        self.table.hideColumn(0)

    def fill_table(self):
        podrs = db.load_all_podr()
        self.table.setRowCount(len(podrs))
        row = 0
        for podr in podrs:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_podr)
            btn.podr = podr
            self.table.setItem(row, 1, QTableWidgetItem(podr.name_podr))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_podr(self):
        self.add_form = AddPodr()
        self.add_form.show()

    def open_change_podr(self):
        sender = self.sender()
        self.change_form = ChangePodr(sender.podr)
        self.change_form.show()


class AddPodr(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить подразделение')
        self.resize(300, 100)
        self.label = QLabel('Введите имя:')
        self.name_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)
        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_podr)
        self.main_layout.addWidget(self.add_btn, 1, 0, 1, 2)

    def add_podr(self):
        pass


class ChangePodr(AddPodr):
    def __init__(self, podr):
        super().__init__()
        self.setWindowTitle('Изменить подразделение')
        self.add_btn.setText('Сохранить')
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(podr.name_podr)
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_podr)

    def add_podr(self):
        pass

    def save_podr(self):
        pass


class SetupSpec(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        self.btns_layout.addWidget(self.add_btn)
        self.btns_layout.addWidget(self.close_btn)

    def init_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(('id', 'Название', ''))
        self.table.hideColumn(0)

    def fill_table(self):
        specs = db.load_all_spec()
        self.table.setRowCount(len(specs))
        row = 0
        for spec in specs:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_spec)
            btn.spec = spec
            self.table.setItem(row, 1, QTableWidgetItem(spec.name_spec))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_spec(self):
        self.add_form = AddSpec()
        self.add_form.show()

    def open_change_spec(self):
        sender = self.sender()
        self.change_form = ChangeSpec(sender.spec)
        self.change_form.show()


class AddSpec(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        pass


class ChangeSpec(AddSpec):
    def __init__(self, spec):
        super().__init__()
        self.setWindowTitle('Изменить специальность')
        self.add_btn.setText('Сохранить')
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(spec.name_spec)
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_spec)

    def add_spec(self):
        pass

    def save_spec(self):
        pass


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
