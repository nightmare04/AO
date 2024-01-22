from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from modules import ListControlM


class Listlk(QtWidgets.QWidget):
    def __init__(self, main):
        super().__init__()
        self.main_window = main
        self.resize(900, 400)
        self.setWindowTitle('Листы контроля')
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QTableWidget()
        self.init_table()
        self.lks = list(ListControlM.select())
        self.fill_table()

    def init_table(self):
        self.main_layout.addWidget(self.table)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Телеграмма",
            "Дата телеграммы",
            "Срок выполнения",
            "Лист контроля",
            "Ответ",
            "Дата ответа",
            "Выполнено",
            ""
        ])

    def fill_table(self):
        self.table.setRowCount(len(self.lks))
        row = 0
        for listk in self.lks:
            btn = QPushButton("Изменить")
            btn.lk = listk
            btn.clicked.connect(self.main_window.open_edit_form)

            if listk.complete_flag:
                complete = "Выполнено"
            else:
                complete = "Не выполнено"

            if listk.answer_date is None:
                answer_date = QtWidgets.QTableWidgetItem('')
            else:
                answer_date = QtWidgets.QTableWidgetItem(str(listk.answer_date.strftime("%d.%m.%Y")))

            listk: ListControlM
            self.table.setItem(row, 0, QTableWidgetItem(str(listk.telegram)))
            self.table.setItem(row, 1, QTableWidgetItem(str(listk.date_telegram.strftime("%d.%m.%Y"))))
            self.table.setItem(row, 2, QTableWidgetItem(str(listk.date_deadline.strftime("%d.%m.%Y"))))
            self.table.setItem(row, 3, QTableWidgetItem(str(listk.number_lk)))
            self.table.setItem(row, 4, QTableWidgetItem(str(listk.answer)))
            self.table.setItem(row, 5, QTableWidgetItem(answer_date))
            self.table.setItem(row, 6, QTableWidgetItem(complete))
            self.table.setCellWidget(row, 7, btn)
            row += 1
