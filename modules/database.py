import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord
from PyQt6.QtWidgets import QMessageBox
from modules.plane import *
from modules.lk import *


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

    def load_data_by_query(self, text: str) -> list:
        self.con.open()
        query = QSqlQuery()
        query.exec(text)
        record = []
        while query.next():
            record.append(query.record())
        self.con.close()
        return record

    def load_all_planes(self) -> list:
        self.con.open()
        result = []
        query = QSqlQuery()
        query.exec("SELECT * FROM planes")
        while query.next():
            plane = Plane()
            plane.unpack_plane(query.record())
            result.append(plane)
        return result

    def add_lk_to_db(self, data: LK):
        pass