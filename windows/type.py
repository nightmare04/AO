from PyQt6 import QtWidgets, QtCore
from modules import PlaneTypeM


class SetupType(QtWidgets.QDialog):
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
        types = PlaneTypeM.select()
        self.table.setRowCount(len(types))
        row = 0
        for t in types:
            btn = QtWidgets.QPushButton('Изменить')
            btn.clicked.connect(self.open_change_type)
            btn.type = t
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(t.name)))
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
        self.type = PlaneTypeM()
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить тип самолета')
        self.resize(300, 100)
        self.label = QtWidgets.QLabel('Введите тип:')
        self.name_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_type)
        self.main_layout.addWidget(self.add_btn, 1, 0, 1, 2)

    def add_type(self):
        self.type.name = self.name_edit.text()
        self.type.save()
        self.close()


class EditType(AddType):
    def __init__(self, t):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Изменить тип самолета')
        self.add_btn.setText('Сохранить')
        self.type = t
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(self.type.name)
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_type)
        self.del_btn = QtWidgets.QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_type)
        self.main_layout.addWidget(self.del_btn, 2, 0, 1, 2)

    def save_type(self):
        self.type.name = self.name_edit.text()
        self.type.save()
        self.close()

    def del_type(self):
        self.type.delete_instance()
        self.close()