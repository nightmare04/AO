from PyQt6 import QtWidgets, QtCore
from modules import SubunitM, PlaneTypeM


class SetupSubunit(QtWidgets.QDialog):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.add_form = None
        self.change_form = None
        self.setWindowTitle("Специальности")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QtWidgets.QTableWidget()
        self.init_table()
        self.fill_table()
        self.main_layout.addWidget(self.table)
        self.btns_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.btns_layout)
        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.open_add_subunit)
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
        self.table.setHorizontalHeaderLabels(('Наименование', 'Тип АТ', ''))

    # noinspection PyUnresolvedReferences
    def fill_table(self):
        subunits = SubunitM.select()
        self.table.setRowCount(len(subunits))
        row = 0
        for subunit in subunits:
            btn = QtWidgets.QPushButton('Изменить')
            btn.clicked.connect(self.open_change_subunit)
            btn.subunit = subunit
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(subunit.name)))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(
                PlaneTypeM.get(PlaneTypeM.id == subunit.plane_type).name))
                               )
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_subunit(self):
        self.add_form = AddSubunit()
        self.add_form.show()

    # noinspection PyUnresolvedReferences
    def open_change_subunit(self):
        sender = self.sender()
        self.change_form = EditSubunit(sender.subunit)
        self.change_form.show()


class AddSubunit(QtWidgets.QWidget):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.subunit = SubunitM()
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить специальность')
        self.resize(300, 100)

        self.label = QtWidgets.QLabel('Введите название:')
        self.name_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)

        self.type_label = QtWidgets.QLabel('Выберите тип АТ:')
        self.type_select = QtWidgets.QComboBox()
        types_list = list(PlaneTypeM.select(PlaneTypeM.name).execute())
        types_names = map(lambda q: q.name, types_list)
        self.type_select.addItems(types_names)
        self.main_layout.addWidget(self.type_label, 1, 0)
        self.main_layout.addWidget(self.type_select, 1, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_unit)
        self.main_layout.addWidget(self.add_btn, 2, 0, 1, 2)

    def add_unit(self):
        self.subunit.name = self.name_edit.text()
        self.subunit.plane_type = PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText())
        self.subunit.save()
        self.close()


class EditSubunit(AddSubunit):
    # noinspection PyUnresolvedReferences
    def __init__(self, s):
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Изменить специальность')
        self.add_btn.setText('Сохранить')
        self.subunit = s
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(str(s.name))
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_subunit)
        self.del_btn = QtWidgets.QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_unit)
        self.main_layout.addWidget(self.del_btn, 3, 0, 1, 2)
        self.type_select.setCurrentText(str(PlaneTypeM.get(PlaneTypeM.id == self.subunit.plane_type).name))

    def save_subunit(self):
        self.subunit.name = self.name_edit.text()
        self.subunit.plane_type = PlaneTypeM.get(PlaneTypeM.name == self.type_select.currentText())
        self.subunit.save()
        self.close()

    def del_unit(self):
        self.subunit.delete_instance()
        self.close()
