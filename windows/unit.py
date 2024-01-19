from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QLabel, QLineEdit, QCheckBox
from modules import UnitM


class SetupUnit(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(280, 400)
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
        self.add_btn.clicked.connect(self.open_add_unit)
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
        units = UnitM.select()
        self.table.setRowCount(len(units))
        row = 0
        for p in units:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_unit)
            btn.unit = p
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_unit(self):
        self.add_form = AddUnit()
        self.add_form.show()

    def open_change_unit(self):
        sender = self.sender()
        self.change_form = EditUnit(sender.podr)
        self.change_form.show()


class AddUnit(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.unit = UnitM()
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
        self.with_planes.setChecked(True)
        self.main_layout.addWidget(self.planes_label, 1, 0)
        self.main_layout.addWidget(self.with_planes, 1, 1)

        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_unit)
        self.main_layout.addWidget(self.add_btn, 2, 0, 1, 2)

    def add_unit(self):
        self.unit.name = self.name_edit.text()
        self.unit.performs_work = self.with_planes.isChecked()
        self.unit.save()
        self.close()


class EditUnit(AddUnit):
    def __init__(self, p):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.unit = p
        p: UnitM
        self.setWindowTitle('Изменить подразделение')
        self.add_btn.setText('Сохранить')

        self.label.setText('Введите новое имя:')
        self.name_edit.setText(p.name)

        self.with_planes.setChecked(p.performs_work)

        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_unit)

        self.del_btn = QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_unit)
        self.main_layout.addWidget(self.del_btn, 4, 0, 1, 2)

    def save_unit(self):
        self.unit: UnitM
        self.unit.name = self.name_edit.text()
        self.unit.performs_work = self.with_planes.isChecked()
        self.unit.save()
        self.close()

    def del_unit(self):
        self.unit: UnitM
        self.unit.delete_instance()
        self.close()
