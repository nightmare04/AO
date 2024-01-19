from PyQt6 import QtWidgets, QtCore
from modules import AgregateM, SystemM, DefectiveM, RemovedM, PlaneTypeM, SubunitM
from .agregate import Agregate


class Systems(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Системы')

        self.resize(500, 500)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.new_form = None

        self.table = QtWidgets.QTableWidget()
        self.main_layout.addWidget(self.table)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название', 'Тип самолета', '', ''])
        self.table.sortByColumn(1, QtCore.Qt.SortOrder.AscendingOrder)
        self.fill_table()

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_system)
        self.main_layout.addWidget(self.add_btn)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def add_system(self):
        self.new_form = AddSystem()
        self.new_form.show()

    def fill_table(self):
        systems = SystemM.select().join(PlaneTypeM)
        self.table.setRowCount(len(systems))
        row = 0
        for system in systems:
            system_name = QtWidgets.QTableWidgetItem(system.name)
            plane_type = QtWidgets.QTableWidgetItem(system.plane_type.name)

            btn_chg = QtWidgets.QPushButton('Изменить')
            btn_chg.clicked.connect(self.change_system)
            btn_chg.system = system

            btn_agr = QtWidgets.QPushButton('Блоки/Агр')
            btn_agr.clicked.connect(self.open_agr)
            btn_agr.system = system

            self.table.setItem(row, 0, system_name)
            self.table.setItem(row, 1, plane_type)
            self.table.setCellWidget(row, 2, btn_chg)
            self.table.setCellWidget(row, 3, btn_agr)
            row += 1

    def change_system(self):
        sender = self.sender()
        self.new_form = ChangeSystem(sender.system)
        self.new_form.show()

    def open_agr(self):
        sender = self.sender()
        self.new_form = Agregate(sender.system)
        self.new_form.show()


class AddSystem(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить систему')
        self.resize(100, 200)
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)

        self.name_label = QtWidgets.QLabel('Наименование системы:')
        self.name_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.name_label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)

        self.type_label = QtWidgets.QLabel('Выберите тип:')
        self.type_select = QtWidgets.QComboBox()
        types_list = list(PlaneTypeM.select(PlaneTypeM.name).execute())
        types_names = map(lambda q: q.name, types_list)
        self.type_select.addItems(types_names)
        self.main_layout.addWidget(self.type_label, 1, 0)
        self.main_layout.addWidget(self.type_select, 1, 1)
        self.type_select.currentTextChanged.connect(self.fill_subunits)

        self.spec_label = QtWidgets.QLabel('Выберите специальность:')
        self.subunit_select = QtWidgets.QComboBox()
        self.main_layout.addWidget(self.spec_label, 2, 0)
        self.main_layout.addWidget(self.subunit_select, 2, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_system)
        self.main_layout.addWidget(self.add_btn, 3, 0, 1, 2)

        self.fill_subunits()

    def fill_subunits(self):
        self.subunit_select.clear()

        subunits_list = list(SubunitM.select().where(
            SubunitM.plane_type == PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText())))
        subunits_names = map(lambda q: q.name, subunits_list)
        self.subunit_select.addItems(subunits_names)

    def add_system(self):
        new_system = SystemM()
        new_system.name = self.name_edit.text()
        new_system.subunit_type = SubunitM.get(SubunitM.name == self.subunit_select.currentText()).id
        new_system.plane_type = PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText()).id
        new_system.save()
        self.close()


class ChangeSystem(AddSystem):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.setWindowTitle('Изменить систему')
        self.name_edit.setText(self.system.name)
        self.type_select.setCurrentText(PlaneTypeM.get(PlaneTypeM.id == self.system.plane_type.id).name)
        self.add_btn.setText('Сохранить')
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_system)

        self.del_btn = QtWidgets.QPushButton('Удалить')
        self.del_btn.clicked.connect(self.del_system)
        self.main_layout.addWidget(self.del_btn, 3, 0, 1, 2)

    def del_system(self):
        self.system.delete_instance()
        self.close()

    def save_system(self):
        self.system.name = self.name_edit.text()
        self.system.plane_type = PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText()).id
        self.system.save()
        self.close()
