from PyQt6.QtWidgets import QGridLayout, QTableWidgetItem, QPushButton, QGroupBox, QHBoxLayout
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
        self.db = Database()
        self.add_lk_form = None
        self.edit_form = None
        self.lks = []
        self.init_table()
        self.fill_table()
        self.ui.add_btn.clicked.connect(self.add_form)
        self.setWindowTitle("Старший инженер по специальности")
        self.show()
        self.db.check_connection()

    def init_table(self):
        """Описываем параметры таблицы долгов"""
        self.lks = self.db.load_all_lk()
        self.ui.tableWidget.setColumnCount(len(LK().__dict__)+2)
    #     {'id_lk' 'tlg' 'date_tlg, 'srok_tlg', 'opisanie' 'lk': 'otvet',
    #     'date_otvet':, 'komu_planes', 'komu_spec':, 'complete'}
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
            "",
            ""
        ])
        self.ui.tableWidget.hideColumn(0)
        self.ui.tableWidget.hideColumn(4)
        self.ui.tableWidget.hideColumn(6)
        self.ui.tableWidget.hideColumn(7)
        self.ui.tableWidget.hideColumn(8)
        self.ui.tableWidget.hideColumn(9)
        self.ui.tableWidget.hideColumn(10)
        self.ui.tableWidget.setRowCount(len(self.lks))

    def fill_table(self):
        """Заполняем таблицу долгами"""
        row = 0
        for listkontr in self.lks:
            btn = QPushButton("Изменить")
            btn.lk = listkontr
            btn.clicked.connect(self.open_edit_form)
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(listkontr.id_lk)))
            self.ui.tableWidget.setCellWidget(row, 11, btn)
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(listkontr.tlg)))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(listkontr.date_tlg)))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(listkontr.srok_tlg)))
            self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(str(listkontr.lk)))
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
        self.spec_btns = []
        self.plane_btns = []
        self.plane_groups = []
        self.ui = Ui_Add_lk_form()
        self.ui.setupUi(self)
        self.ui.TlgDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.SrokDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.add_btn.clicked.connect(self.add_lk_to_db)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.init_planes()
        self.init_spec()

    def init_planes(self):
        """Готовим самолеты"""
        all_podr = main.db.load_all_podr()
        for p in all_podr:
            row_plane = 0
            col_plane = 0
            groupbox = QGroupBox(p.name_podr)
            self.ui.planesLayout.addWidget(groupbox)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.setCheckable(True)
            groupbox.podrazd = p
            groupbox.plane_btns = []
            groupbox.toggled.connect(self.check_toggle)
            self.plane_groups.append(groupbox)
            for planes in main.db.load_planes_by_podr(p.id_podr):
                btn = QPushButton(text=str(planes.bort_num))
                btn.setFixedWidth(30)
                btn.setCheckable(True)
                btn.plane = planes
                btn.setChecked(True)
                self.plane_btns.append(btn)
                if col_plane < 3:
                    layout_planes.addWidget(btn, row_plane, col_plane)
                    groupbox.plane_btns.append(btn)
                    col_plane += 1
                else:
                    row_plane += 1
                    col_plane = 0
                    groupbox.plane_btns.append(btn)
                    layout_planes.addWidget(btn, row_plane, col_plane)

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
        all_spec = main.db.load_all_spec()
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
        data.pack_lk_from_form(self)
        main.db.add_lk_to_db(data)
        self.close()


class EditLK(AddLk):
    def __init__(self, listkontr):
        super().__init__()
        self.lk = listkontr
        self.setWindowTitle("Изменить")
        self.ui.add_btn.setText("Сохранить")
        self.ui.add_btn.clicked.connect(self.save_lk)
        self.ui.cancel_btn.setText("Удалить")
        self.ui.cancel_btn.clicked.connect(self.delete_lk)
        self.load_lk()

    def load_lk(self):
        """Подгружаем лист контроля"""
        self.ui.TlgLineEdit.setText(self.lk.tlg)
        self.ui.TlgDateEdit.setDate(QDate(datetime.strptime(self.lk.date_tlg, '%Y-%m-%d')))

    def save_lk(self):
        pass

    def delete_lk(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys

    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    main = MainWindow()
    sys.exit(app.exec())
