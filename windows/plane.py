from PyQt6 import QtWidgets, QtCore
from modules import PlaneModel


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

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def init_table(self):
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Тип', 'Бортовой номер', 'Заводской номер', ''))

    def fill_table(self):
        planes = PlaneModel.select()
        self.table.setRowCount(len(planes))
        row = 0
        for p in planes:
            btn = QtWidgets.QPushButton('Изменить')
            btn.clicked.connect(self.open_change_plane)
            btn.plane = p
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem())
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem())
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem())
            self.table.setCellWidget(row, 3, btn)

            row += 1

    def open_add_plane(self):
        self.add_form = AddPlane(self.db)
        self.add_form.show()

    def open_change_plane(self):
        sender = self.sender()
        self.change_form = EditPlane(sender.plane, self.db)
        self.change_form.show()


class AddPlane(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.plane = Plane()
        self.types = {}
        self.podrs = {}
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить самолет')
        self.resize(300, 100)

        self.label = QtWidgets.QLabel('Выберите тип:')
        self.type_select = QtWidgets.QComboBox()
        self.add_types_combo()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.type_select, 0, 1)

        self.label = QtWidgets.QLabel('Выберите подразделение:')
        self.podr_select = QtWidgets.QComboBox()
        self.add_podr_combo()
        self.main_layout.addWidget(self.label, 1, 0)
        self.main_layout.addWidget(self.podr_select, 1, 1)

        self.label = QtWidgets.QLabel('Бортовой номер:')
        self.bort_num_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.label, 2, 0)
        self.main_layout.addWidget(self.bort_num_edit, 2, 1)

        self.label = QtWidgets.QLabel('Заводской номер:')
        self.zav_num_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.label, 3, 0)
        self.main_layout.addWidget(self.zav_num_edit, 3, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_plane)
        self.main_layout.addWidget(self.add_btn, 4, 0, 1, 2)

    def add_podr_combo(self):
        podrs = self.db.load_all_podr()
        res_podr = []
        for p in podrs:
            self.podrs[p.name_podr] = p.id_podr
            res_podr.append(p.name_podr)
        self.podr_select.addItems(res_podr)

    def add_types_combo(self):
        types = self.db.load_all_type()
        res_type = []
        for t in types:
            self.types[t.name_type] = t.id_type
            res_type.append(t.name_type)
        self.type_select.addItems(res_type)

    def add_plane(self):
        self.plane.pack_plane(self)
        self.db.add_plane(self.plane)
        self.close()


class EditPlane(AddPlane):
    def __init__(self, p, db):
        super().__init__(db)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.plane = Plane().unpack_plane(p)
        self.setWindowTitle('Изменить самолет')

        self.add_btn.setText('Сохранить')
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_plane)

        self.del_btn = QtWidgets.QPushButton('Удалить')
        self.del_btn.clicked.connect(self.del_plane)
        self.main_layout.addWidget(self.del_btn, 5, 0, 1, 2)

        self.fill_plane()

    def fill_plane(self):
        self.bort_num_edit.setText(str(self.plane.bort_num))
        self.zav_num_edit.setText(str(self.plane.zav_num))
        # self.type_select.setCurrentIndex(self.type_select.findText(db.load_type_by_id(self.plane.id_type)))

    def save_plane(self):
        self.plane.pack_plane(self)
        self.db.update_plane(self.type)
        self.close()

    def del_plane(self):
        self.db.delete_plane(self.plane.id_plane)
        self.close()
