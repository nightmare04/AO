from PyQt6 import QtWidgets, QtCore
from modules import AgregateM, SystemM, DefectiveM, RemovedM, PlaneTypeM


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
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Название', 'Тип самолета', ''])
        self.table.sortByColumn(1, QtCore.Qt.SortOrder.AscendingOrder)
        self.fill_table()

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_system)
        self.main_layout.addWidget(self.add_btn)

    def add_system(self):
        self.new_form = AddSystem()
        self.new_form.show()

    def fill_table(self):
        systems = SystemM.select(SystemM.name, PlaneTypeM.name).join(PlaneTypeM)
        self.table.setRowCount(len(systems))
        row = 0
        for system in systems:
            system_name = QtWidgets.QTableWidgetItem(system.name)
            plane_type = QtWidgets.QTableWidgetItem(system.plane_type.name)
            btn = QtWidgets.QPushButton('Изменить')
            btn.clicked.connect(self.change_system)
            btn.system = system
            self.table.setItem(row, 0, system_name)
            self.table.setItem(row, 1, plane_type)
            self.table.setCellWidget(row, 2, btn)
            row += 1

    def change_system(self):
        pass


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
        query = list(PlaneTypeM.select(PlaneTypeM.name).execute())
        self.type_select.addItems(map(lambda q: q.name, query))
        self.main_layout.addWidget(self.type_label, 1, 0)
        self.main_layout.addWidget(self.type_select, 1, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_system)
        self.main_layout.addWidget(self.add_btn, 2, 0, 1, 2)

    def add_system(self):
        new_system = SystemM()
        new_system.name = self.name_edit.text()
        new_system.plane_type = PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText()).id
        new_system.save()
        self.close()
