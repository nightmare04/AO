from PyQt6 import QtWidgets


class Listlk(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.resize(900, 400)
        self.setWindowTitle('Листы контроля')
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = QTableWidget()
        self.init_table()
        self.lks = self.db.load_all_lk()
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
            btn.clicked.connect(main.open_edit_form)

            if listk.complete:
                complete = "Выполнено"
            else:
                complete = "Не выполнено"

            self.table.setItem(row, 0, QTableWidgetItem(str(listk.tlg)))
            self.table.setItem(row, 1, QTableWidgetItem(str(listk.date_tlg)))
            self.table.setItem(row, 2, QTableWidgetItem(str(listk.date_vypoln)))
            self.table.setItem(row, 3, QTableWidgetItem(str(listk.lk)))
            self.table.setItem(row, 4, QTableWidgetItem(str(listk.otvet)))
            self.table.setItem(row, 5, QTableWidgetItem(str(listk.date_otvet)))
            self.table.setItem(row, 6, QTableWidgetItem(complete))
            self.table.setCellWidget(row, 7, btn)
            row += 1