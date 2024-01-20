from PyQt6 import QtWidgets, QtCore
from modules import AgregateM, SystemM, PlaneTypeM


class Agregate(QtWidgets.QWidget):
    def __init__(self, system: SystemM):
        super().__init__()
        self.system = system
        self.setWindowTitle(f'Блоки / агрегаты системы {system.name} ')

        self.resize(500, 700)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.new_form = None

        self.table = QtWidgets.QTableWidget()
        self.main_layout.addWidget(self.table)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Наименование', 'Кол-во на сам-те', 'Изменить', 'Удалить'])
        self.table.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.fill_table()

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_agregate)
        self.main_layout.addWidget(self.add_btn)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def add_agregate(self):
        self.new_form = AddAgregate(self.system)
        self.new_form.show()

    def fill_table(self):
        agregates = AgregateM.select().where(AgregateM.id_system == self.system.id)
        self.table.setRowCount(len(agregates))
        row = 0
        for agregate in agregates:
            agregate_name = QtWidgets.QTableWidgetItem(agregate.name)
            agregate_amount = QtWidgets.QTableWidgetItem(str(agregate.amount))

            btn_chg = QtWidgets.QPushButton('Изменить')
            btn_chg.clicked.connect(self.change_agr)
            btn_chg.agr = agregate

            btn_del = QtWidgets.QPushButton('Удалить')
            btn_del.clicked.connect(self.del_agr)
            btn_del.agr = agregate

            self.table.setItem(row, 0, agregate_name)
            self.table.setItem(row, 1, agregate_amount)
            self.table.setCellWidget(row, 2, btn_chg)
            self.table.setCellWidget(row, 3, btn_del)
            row += 1

    def del_agr(self):
        sender = self.sender()
        sender.agr.delete_instance()
        self.fill_table()

    def change_agr(self):
        sender = self.sender()
        self.new_form = ChangeAgr(self.system, sender.agr)
        self.new_form.show()


class AddAgregate(QtWidgets.QWidget):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.setWindowTitle('Добавить блок / агрегат')
        self.resize(400, 200)
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)

        self.name_label = QtWidgets.QLabel('Наименование:')
        self.name_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.name_label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)

        self.amount_label = QtWidgets.QLabel('Количество:')
        self.amount_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.amount_label, 1, 0)
        self.main_layout.addWidget(self.amount_edit, 1, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_agr)
        self.main_layout.addWidget(self.add_btn, 2, 0, 1, 2)

    def add_agr(self):
        new_agr = AgregateM()
        new_agr.name = self.name_edit.text()
        new_agr.id_system = self.system.id
        new_agr.amount = int(self.amount_edit.text())
        new_agr.save()
        self.close()


class ChangeAgr(AddAgregate):
    def __init__(self, system, agr):
        super().__init__(system)
        self.system = system
        self.agr = agr
        self.setWindowTitle('Изменить блок / агрегат')
        self.name_edit.setText(self.agr.name)
        self.amount_edit.setText(str(self.agr.amount))

        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_agr)


    def save_agr(self):
        self.agr.name = self.name_edit.text()
        self.agr.id_system = self.system.id
        self.agr.amount = int(self.amount_edit.text())
        self.agr.save()
        self.close()
