import datetime

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QDateEdit, QComboBox, QVBoxLayout,
                             QGridLayout, QLabel)

from modules import CheckModel


class Checks(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 300)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Проверки")
        self.new_window = None

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.table = QTableWidget()
        self.main_layout.addWidget(self.table)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Название', 'Периодичность', 'Дата последней проверки', ''))
        self.table.setColumnWidth(2, 160)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.open_add_form)
        self.main_layout.addWidget(self.add_btn)

        self.all_checks = []
        self.fill_table()

    def event(self, e):
        if e == QtCore.QEvent.Type.WindowUnblocked:
            self.fill_table()
        return QtWidgets.QWidget.event(self, e)

    def open_add_form(self):
        self.new_window = AddCheck()
        self.new_window.show()

    def fill_table(self):
        for check in CheckModel.select():
            self.all_checks.append(check)
        self.table.setRowCount(len(self.all_checks))

        row = 0
        for ch in self.all_checks:
            ch: CheckModel
            btn = QPushButton("Изменить")
            btn.check = ch
            btn.clicked.connect(self.edit_check)
            self.table.setItem(row, 0, QTableWidgetItem(ch.name))
            self.table.setItem(row, 1, QTableWidgetItem(ch.period))
            self.table.setItem(row, 2, QTableWidgetItem(ch.last_check.strftime("%d.%m.%Y")))
            self.table.setCellWidget(row, 3, btn)

            row += 1

    def edit_check(self):
        btn = self.sender()
        self.new_window = EditCheck(btn.check)
        self.new_window.show()


class AddCheck(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 300)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Добавить проверку")
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.check = CheckModel()

        self.name_label = QLabel("Название:")
        self.name_line_edit = QLineEdit()
        self.main_layout.addWidget(self.name_label, 0, 0)
        self.main_layout.addWidget(self.name_line_edit, 0, 1)

        self.period_label = QLabel("Периодичность:")
        self.period_combobox = QComboBox()
        self.period_combobox.addItems(('месяц', 'квартал', 'год'))
        self.main_layout.addWidget(self.period_label, 1, 0)
        self.main_layout.addWidget(self.period_combobox, 1, 1)

        self.last_check_label = QLabel("Дата проверки:")
        self.last_check_date = QDateEdit()
        self.last_check_date.setCalendarPopup(True)
        self.last_check_date.setDate(QtCore.QDate.currentDate())
        self.main_layout.addWidget(self.last_check_label, 2, 0)
        self.main_layout.addWidget(self.last_check_date, 2, 1)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.add_check)
        self.cancel_btn = QPushButton("Закрыть")
        self.cancel_btn.clicked.connect(self.close)
        self.main_layout.addWidget(self.save_btn, 3, 0)
        self.main_layout.addWidget(self.cancel_btn, 3, 1)

    def add_check(self):
        check: CheckModel
        check = CheckModel(
            name=self.name_line_edit.text(),
            last_check=self.last_check_date.date().toPyDate(),
            period=self.period_combobox.currentText()
        )
        check.save()
        self.close()


class EditCheck(AddCheck):
    def __init__(self, ch: CheckModel):
        super().__init__()
        self.check = ch
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Изменить проверку")
        self.name_line_edit.setText(ch.name)
        self.period_combobox.setCurrentText(ch.period)
        self.save_btn.clicked.disconnect()
        self.save_btn.clicked.connect(self.save_check)
        self.cancel_btn.setText('Удалить')
        self.cancel_btn.clicked.disconnect()
        self.cancel_btn.clicked.connect(self.delete_check)
        self.last_check_date.setDate(ch.last_check)

    def save_check(self):
        self.check: CheckModel
        self.check.name = self.name_line_edit.text(),
        self.check.last_check = self.last_check_date.date().toPyDate(),
        self.check.period = str(self.period_combobox.currentText())

        self.check.save()
        self.close()

    def delete_check(self):
        self.check.delete()
        self.close()
