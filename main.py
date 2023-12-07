from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtCore import QDate
from ui import *
from modules import *
import ctypes
from datetime import datetime, date


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_table()
        self.fill_table()
        self.ui.add_btn.clicked.connect(self.add_lk_form)
        self.db = Database()
        self.setWindowTitle("Старший инженер по специальности")
        self.show()
        self.db.check_connection()

    def init_table(self):
        """Описываем параметры таблицы долгов"""
        pass

    def fill_table(self):
        """Заполняем таблицу долгами"""
        pass

    def add_lk_form(self):
        """Открываем новую форму добавления листа контроля"""
        self.addlk = AddLk()
        self.addlk.show()


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
        all_podr = main.db.load_all_podr()
        for podr in all_podr:
            row_plane = 0
            col_plane = 0
            groupbox = QGroupBox(podr.name_podr)
            self.ui.planesLayout.addWidget(groupbox)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.setCheckable(True)
            groupbox.podrazd = podr
            groupbox.plane_btns = []
            groupbox.toggled.connect(self.check_toggle)
            self.plane_groups.append(groupbox)
            for planes in main.db.load_planes_by_podr(podr.id_podr):
                btn = QPushButton(text=str(planes.bort_num))
                btn.setFixedWidth(30)
                btn.setCheckable(True)
                btn.plane = planes
                btn.setChecked(True)
                self.plane_btns.append(btn)
                if col_plane < 3 :
                    layout_planes.addWidget(btn, row_plane, col_plane)
                    groupbox.plane_btns.append(btn)
                    col_plane += 1
                else:
                    row_plane += 1
                    col_plane = 0
                    groupbox.plane_btns.append(btn)
                    layout_planes.addWidget(btn, row_plane, col_plane)

    def check_toggle(self):
        sender = self.sender()
        for btn in sender.plane_btns:
            if sender.isChecked():
                btn.setChecked(True)
            else:
                btn.setChecked(False)


    def init_spec(self):
        all_spec = main.db.load_all_spec()
        groupbox = QGroupBox("Специальности")
        layout_spec = QHBoxLayout()
        groupbox.setLayout(layout_spec)
        self.ui.SpecLayout.addWidget(groupbox)
        for spec in all_spec:
            btn = QPushButton(spec.name_spec)
            btn.setCheckable(True)
            btn.spec = spec
            self.spec_btns.append(btn)
            layout_spec.addWidget(btn)

    def add_lk_to_db(self):
        data = LK()
        data.pack_lk_from_form(self)
        main.db.add_lk_to_db(data)
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys

    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    main = MainWindow()
    sys.exit(app.exec())
