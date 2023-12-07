from PyQt6.QtSql import QSqlDatabase, QSqlQuery
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

    def load_all_lk(self):
        self.con.open()
        result = []
        query = QSqlQuery()
        query.exec("SELECT * from lk")
        while query.next():
            lk = LK()
            lk.unpack_lk_from_db(query.record())
            result.append(lk)
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
        self.con.open()
        query = QSqlQuery()
        query.prepare("""INSERT into lk values (
                        null, :tlg, :date_tlg, :date_vypoln, :opisanie,
                        :lk, null, null, :komu_spec, :komu_planes, :complete)""")
        query.bindValue(':tlg', data.tlg)
        query.bindValue(':date_tlg', data.date_tlg)
        query.bindValue(':date_vypoln', data.srok_tlg)
        query.bindValue(':opisanie', data.opisanie)
        query.bindValue(':lk', data.lk)
        query.bindValue(':komu_spec', json.dumps(data.komu_spec))
        query.bindValue(':komu_planes', json.dumps(data.komu_planes))
        query.bindValue(':complete', 0)
        query.exec()
        self.con.close()

    def update_lk_in_db(self, lk: LK):
        self.con.open()
        query = QSqlQuery()
        query.exec(
            f"UPDATE lk SET tlg='{lk.tlg}', "
            f"date_tlg='{lk.date_tlg}', "
            f"date_vypoln='{lk.srok_tlg}', "
            f"opisanie='{lk.opisanie}', "
            f"lk='{lk.lk}', "
            f"komu_spec='{lk.komu_spec}', "
            f"komu_planes='{lk.komu_planes}', "
            f"complete='{lk.complete}', "
            f"otvet='{lk.otvet}', "
            f"date_otvet='{lk.date_otvet}' "
            f"WHERE id_lk={lk.id_lk}"
        )
        self.con.close()

    def delete_lk(self, lk: LK):
        self.con.open()
        query = QSqlQuery()
        query.exec(f"DELETE from lk WHERE id={lk.id_lk}")
        self.con.close()
