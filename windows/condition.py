from PyQt6 import QtWidgets, QtCore, QtGui
from modules import UnitM, PlaneM, SystemM, AgregateM, SubunitM


class Condition(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Выберите самолет')
        self.resize(700, 500)
        self.new_form = None
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.unit_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.unit_layout)
        self.all_units = UnitM.select().order_by(+UnitM.name)
        self.init_planes()

    def init_planes(self):
        for unit in self.all_units:
            groupbox = QtWidgets.QGroupBox()
            groupbox.setTitle(unit.name)
            plane_layout = QtWidgets.QGridLayout()
            groupbox.setLayout(plane_layout)
            self.unit_layout.addWidget(groupbox)

            planes = PlaneM.select().where(PlaneM.unit == unit.id).order_by(+PlaneM.tail_number)
            row = 0
            col = 0
            for plane in planes:
                plane_btn = QtWidgets.QPushButton(plane.tail_number)
                plane_btn.clicked.connect(self.open_plane_cond)
                plane_btn.plane = plane
                plane_btn.setFixedWidth(30)
                if col < 3:
                    plane_layout.addWidget(plane_btn, row, col)
                    col += 1
                else:
                    col = 0
                    row += 1
                    plane_layout.addWidget(plane_btn, row, col)
                    col += 1

    def open_plane_cond(self):
        sender = self.sender()
        self.new_form = PlaneCondition(sender.plane)
        self.new_form.show()


class PlaneCondition(QtWidgets.QWidget):
    def __init__(self, plane: PlaneM):
        super().__init__()
        self.new_form = None
        self.plane = plane
        self.resize(700, 700)
        self.setWindowTitle(f'Самолет №{self.plane.tail_number}')
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.agr_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.agr_layout)

        self.defect_layout = QtWidgets.QVBoxLayout()
        self.defect_groupbox = QtWidgets.QGroupBox('Неисправные блоки / агрегаты')
        self.defect_groupbox.setLayout(self.defect_layout)
        self.agr_layout.addWidget(self.defect_groupbox)
        self.defect_table = QtWidgets.QTableWidget()
        self.defect_layout.addWidget(self.defect_table)
        self.defect_btn_layout = QtWidgets.QHBoxLayout()
        self.defect_layout.addLayout(self.defect_btn_layout)
        self.defect_add_btn = QtWidgets.QPushButton('Добавить')
        self.defect_add_btn.clicked.connect(self.open_add_defect)
        self.defect_btn_layout.addWidget(self.defect_add_btn)
        self.defect_table.setColumnCount(5)
        self.defect_table.setHorizontalHeaderLabels(['Наименование', 'Система', 'Номер', 'Изменить', 'Удалить'])

        self.removed_layout = QtWidgets.QVBoxLayout()
        self.removed_table = QtWidgets.QTableWidget()
        self.removed_btn_layout = QtWidgets.QHBoxLayout()
        self.removed_groupbox = QtWidgets.QGroupBox('Снятые блоки / агрегаты')
        self.removed_groupbox.setLayout(self.removed_layout)
        self.agr_layout.addWidget(self.removed_groupbox)
        self.removed_add_btn = QtWidgets.QPushButton('Добавить')
        self.removed_add_btn.clicked.connect(self.open_add_removed)
        self.removed_groupbox.layout().addWidget(self.removed_table)
        self.removed_layout.addLayout(self.removed_btn_layout)
        self.removed_btn_layout.addWidget(self.removed_add_btn)
        self.removed_table.setColumnCount(6)
        self.removed_table.setHorizontalHeaderLabels(['Наименование', 'Система', 'Номер',
                                                      'Куда снято', 'Изменить', 'Удалить'])

    def open_add_removed(self):
        pass

    def open_add_defect(self):
        self.new_form = AddDefect(self.plane)
        self.new_form.show()


class AddDefect(QtWidgets.QWidget):
    def __init__(self, plane: PlaneM):
        super().__init__()
        self.setWindowTitle('Добавить неисправный блок')
        self.resize(400, 400)
        self.plane = plane
        self.main_layout = QtWidgets.QVBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)

        self.subunit_name_label = QtWidgets.QLabel('Специальность:')
        self.subunit_name_edit = QtWidgets.QComboBox()
        subunits_list = list(SubunitM.select(SubunitM.name).where(SubunitM.plane_type == self.plane.plane_type))
        subunits_name = map(lambda q: q.name, subunits_list)
        self.subunit_name_edit.addItems(subunits_name)
        self.grid_layout.addWidget(self.subunit_name_label, 0, 0)
        self.grid_layout.addWidget(self.subunit_name_edit, 0, 1)
        self.subunit_name_edit.currentTextChanged.connect(self.fill_systems)

        self.system_name_label = QtWidgets.QLabel('Система:')
        self.system_name_edit = QtWidgets.QComboBox()
        systems_list = list(SystemM.select(SystemM.name).
                            where(SystemM.plane_type == self.plane.plane_type,
                                  SystemM.subunit_type == SubunitM.get(SubunitM.name ==
                                                                       self.subunit_name_edit.currentText()).id))
        systems_name = map(lambda q: q.name, systems_list)
        self.system_name_edit.addItems(systems_name)
        self.grid_layout.addWidget(self.system_name_label, 1, 0)
        self.grid_layout.addWidget(self.system_name_edit, 1, 1)
        self.system_name_edit.currentTextChanged.connect(self.fill_agr)

        self.agr_label = QtWidgets.QLabel('Выберите блок / агрегат:')
        self.agr_select = QtWidgets.QComboBox()
        agrs_list = list(AgregateM.select().where(AgregateM.id_system == SystemM.get(SystemM.name == self.system_name_edit.currentText()).id))
        agrs_name = map(lambda q: q.name, agrs_list)
        self.agr_select.addItems(agrs_name)
        self.grid_layout.addWidget(self.agr_label, 2, 0)
        self.grid_layout.addWidget(self.agr_select, 2, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_defect)
        self.grid_layout.addWidget(self.add_btn, 3, 0, 1, 2)

    def fill_systems(self):
        self.system_name_edit.clear()
        systems_list = list(SystemM.select(SystemM.name).
                            where(SystemM.plane_type == self.plane.plane_type,
                                  SystemM.subunit_type == SubunitM.get(SubunitM.name ==
                                                                       self.subunit_name_edit.currentText()).id))
        systems_name = map(lambda q: q.name, systems_list)
        self.system_name_edit.addItems(systems_name)

    def fill_agr(self):
        self.agr_select.clear()
        agrs_list = list(AgregateM.select().where(
            AgregateM.id_system == SystemM.get(SystemM.name == self.system_name_edit.currentText()).id))
        agrs_name = map(lambda q: q.name, agrs_list)
        self.agr_select.addItems(agrs_name)

    def add_defect(self):
        pass
