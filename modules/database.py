import sys
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox


class Database:
    def __init__(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("./database/ias.db")

    def check_connection(self):
        if not self.con.open():
            QMessageBox.critical(
                None, "Ошибка базы данных",
                "Database Error: %s" % self.con.lastError().databaseText(),
            )

