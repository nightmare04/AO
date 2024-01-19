from PyQt6 import QtWidgets, QtCore
from modules import PlaneM, UnitM, PlaneTypeM


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
        self.default_unit = ''

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def init_table(self):
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Тип', 'Бортовой номер', 'Подразделение', ''))

    def fill_table(self):
        planes = PlaneM.select().where(PlaneM.deleted == False).join(PlaneTypeM)
        self.table.setRowCount(len(planes))
        row = 0
        for p in planes:
            btn = QtWidgets.QPushButton('Изменить')
            btn.clicked.connect(self.open_change_plane)
            btn.plane = p
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p.plane_type.name)))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p.tail_number)))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p.unit.name)))
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
        self.plane = PlaneM()
        self.types = {}
        self.units = {}
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить самолет')
        self.resize(300, 100)

        self.type_label = QtWidgets.QLabel('Выберите тип:')
        self.type_select = QtWidgets.QComboBox()
        self.add_types_combo()
        self.main_layout.addWidget(self.type_label, 0, 0)
        self.main_layout.addWidget(self.type_select, 0, 1)

        self.unit_label = QtWidgets.QLabel('Выберите подразделение:')
        self.unit_select = QtWidgets.QComboBox()
        self.add_unit_combo()
        self.main_layout.addWidget(self.unit_label, 1, 0)
        self.main_layout.addWidget(self.unit_select, 1, 1)

        self.tail_number_label = QtWidgets.QLabel('Бортовой номер:')
        self.tail_number_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.tail_number_label, 2, 0)
        self.main_layout.addWidget(self.tail_number_edit, 2, 1)

        self.factory_number_label = QtWidgets.QLabel('Заводской номер:')
        self.factory_number_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.factory_number_label, 3, 0)
        self.main_layout.addWidget(self.factory_number_edit, 3, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_plane)
        self.main_layout.addWidget(self.add_btn, 4, 0, 1, 2)

    def add_unit_combo(self):
        units = UnitM.select()
        res_unit = []
        for p in units:
            res_unit.append(p.name)
        self.unit_select.addItems(res_unit)

    def add_types_combo(self):
        types = PlaneTypeM.select()
        res_type = []
        for t in types:
            res_type.append(str(t.name))
        self.type_select.addItems(res_type)

    def add_plane(self):
        self.plane.unit = str(UnitM.get(UnitM.name == self.unit_select.currentText()))
        self.plane.plane_type = str(PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText()))
        self.plane.tail_number = self.tail_number_edit.text()
        self.plane.factory_number = self.zav_num_edit.text()
        self.plane.save()
        self.close()


class EditPlane(AddPlane):
    def __init__(self, p):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.plane = p
        self.setWindowTitle('Изменить самолет')

        self.add_btn.setText('Сохранить')
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.add_plane)

        self.del_btn = QtWidgets.QPushButton('Удалить')
        self.del_btn.clicked.connect(self.del_plane)
        self.main_layout.addWidget(self.del_btn, 5, 0, 1, 2)

        self.fill_plane()

    def fill_plane(self):
        self.tail_number_edit.setText(str(self.plane.tail_number))
        self.zav_num_edit.setText(str(self.plane.factory_number))
        self.type_select.setCurrentText(PlaneTypeM.get(PlaneTypeM.id == self.plane.plane_type).name)
        # self.type_select.setCurrentIndex(self.type_select.findText(db.load_type_by_id(self.plane.id_type)))

    def del_plane(self):
        self.plane.deleted = True
        self.plane.save()
        self.close()
