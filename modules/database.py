import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord
from PyQt6.QtWidgets import QMessageBox

from modules.spec import *
from modules.podr import *
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
            self.con.close()

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
        self.con.close()
        return result

    def load_all_podr(self) -> list:
        self.con.open()
        result = []
        query = QSqlQuery()
        query.exec("SELECT * FROM podr")
        while query.next():
            podr = Podr()
            podr.unpack_podr(query.record())
            result.append(podr)
        self.con.close()
        return result

    def load_all_spec(self) -> list:
        self.con.open()
        result = []
        query = QSqlQuery()
        query.exec("SELECT * FROM spec")
        while query.next():
            spec = Spec()
            spec.unpack_podr(query.record())
            result.append(spec)
        self.con.close()
        return result

    def load_planes_by_podr(self, id_podr) -> list:
        self.con.open()
        result = []
        query = QSqlQuery()
        query.exec(f"SELECT * FROM planes WHERE id_podr={id_podr}")
        while query.next():
            plane = Plane()
            plane.unpack_plane(query.record())
            result.append(plane)
        self.con.close()
        return result

    def add_lk_to_db(self, data: LK):
        pass
