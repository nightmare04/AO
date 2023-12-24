from PyQt6 import QtWidgets


class SetupSpec(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
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
        self.add_btn.clicked.connect(self.open_add_spec)
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
        specs = self.db.load_all_spec()
        self.table.setRowCount(len(specs))
        row = 0
        for s in specs:
            btn = QPushButton('Изменить')
            btn.clicked.connect(self.open_change_spec)
            btn.spec = s
            self.table.setItem(row, 1, QTableWidgetItem(str(s.name_spec)))
            self.table.setCellWidget(row, 2, btn)

            row += 1

    def open_add_spec(self):
        self.add_form = AddSpec()
        self.add_form.show()

    def open_change_spec(self):
        sender = self.sender()
        self.change_form = EditSpec(sender.spec)
        self.change_form.show()


class AddSpec(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.spec = Spec()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f'Добавить специальность')
        self.resize(300, 100)

        self.label = QLabel('Введите имя:')
        self.name_edit = QLineEdit()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.name_edit, 0, 1)

        self.add_btn = QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_spec)
        self.main_layout.addWidget(self.add_btn, 1, 0, 1, 2)

    def add_spec(self):
        self.spec.pack_spec(self)
        self.db.add_spec(self.spec)
        self.close()

class EditSpec(AddSpec):
    def __init__(self, s, db):
        super().__init__(db)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Изменить специальность')
        self.add_btn.setText('Сохранить')
        self.spec = s
        self.label.setText('Введите новое имя:')
        self.name_edit.setText(str(s.name_spec))
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.save_spec)
        self.del_btn = QPushButton("Удалить")
        self.del_btn.clicked.connect(self.del_spec)
        self.main_layout.addWidget(self.del_btn, 2, 0, 1, 2)

    def save_spec(self):
        self.spec.pack_spec(self)
        self.db.update_spec(self.spec)
        self.close()

    def del_spec(self):
        self.db.delete_spec(self.spec.id_spec)
        self.close()