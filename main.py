from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QGroupBox, QVBoxLayout, QGridLayout
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
        self.ico = QtGui.QIcon("ui/main.ico")
        self.setWindowIcon(self.ico)

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
        self.ui = Ui_Add_lk_form()
        self.ui.setupUi(self)
        self.ui.TlgDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.SrokDateEdit.setDate(QtCore.QDate().currentDate())

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())