import json

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

from modules.spec import *
from modules.podr import *
from modules.plane import *
from modules.type import *
from modules.lk import *


class Database:
    def __init__(self):
        super(Database, self).__init__()

    @staticmethod
    def create_connection():
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("./database/ias.db")

        if not db.open():
            QMessageBox.critical(
                None, "Ошибка базы данных",
                "Database Error: %s" % db.lastError().databaseText(), QMessageBox.Cancel
            )
            return False

        # TODO Create query to create all tables
        return True

    @staticmethod
    def query_wp(sql_query, query_values=None):
        query = QSqlQuery()
        query.prepare(sql_query)
        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()
        return query

    def load_all(self, table) -> QSqlQuery:
        query_text = f"SELECT * FROM {table}"
        query = self.query_wp(query_text)
        return query

    def load_all_lk(self) -> list:
        result = []
        query = self.load_all('lk')
        while query.next():
            lk = LK()
            lk.unpack_lk(query.record())
            result.append(lk)
        return result

    def load_all_podr(self) -> list:
        result = []
        query = self.load_all('podr')
        while query.next():
            podr = Podr()
            podr.unpack_podr(query.record())
            result.append(podr)
        return result

    def load_all_planes(self) -> list:
        result = []
        query = self.load_all('planes')
        while query.next():
            plane = Plane()
            plane.unpack_plane(query.record())
            result.append(plane)
        return result

    def load_all_planes_table(self) -> list:
        result = []
        query_text = ("SELECT planes.id_plane, planes_type.name_type, planes.bort_num, planes.zav_num, podr.name_podr "
                      "FROM planes "
                      "INNER JOIN planes_type "
                      "ON planes.id_type = planes_type.id_type "
                      "INNER JOIN podr "
                      "ON planes.id_podr = podr.id_podr")
        query = self.query_wp(query_text)
        while query.next():
            result.append(query.record())
        return result

    def load_all_spec(self) -> list:
        result = []
        query = self.load_all('spec')
        while query.next():
            spec = Spec()
            spec.unpack_spec(query.record())
            result.append(spec)
        return result

    def load_plane(self, id_plane):
        query = self.query_wp(f"SELECT * FROM planes WHERE id_plane={id_plane}")
        query.next()
        return query.record()

    def load_lk(self, id_lk):
        query_text = f"SELECT * FROM lk WHERE id_lk={id_lk}"
        query = self.query_wp(query_text)
        query.next()

        return query.record()

    @staticmethod
    def add_lk(data: LK):
        query = QSqlQuery()
        query.prepare("""INSERT into lk values (
                        null, :tlg, :date_tlg, :date_vypoln, :opisanie,
                        :lk, null, null, :komu_spec, :komu_planes, :complete, :planes)""")
        query.bindValue(':tlg', data.tlg)
        query.bindValue(':date_tlg', data.date_tlg)
        query.bindValue(':date_vypoln', data.date_vypoln)
        query.bindValue(':opisanie', data.opisanie)
        query.bindValue(':lk', data.lk)
        query.bindValue(':komu_spec', json.dumps(data.komu_spec))
        query.bindValue(':komu_planes', json.dumps(data.komu_planes))
        query.bindValue(':complete', 0)
        query.bindValue(':planes', json.dumps(data.planes))
        query.exec()

    @staticmethod
    def update_lk(lk: LK):
        query = QSqlQuery()
        query_text = (f"UPDATE lk SET "
                      f"tlg='{lk.tlg}', "
                      f"date_tlg='{lk.date_tlg}', "
                      f"date_vypoln='{lk.date_vypoln}', "
                      f"opisanie='{lk.opisanie}', "
                      f"lk='{lk.lk}', "
                      f"komu_spec='{lk.komu_spec}', "
                      f"komu_planes='{lk.komu_planes}', "
                      f"complete='{lk.complete}', "
                      f"otvet='{lk.otvet}', "
                      f"date_otvet='{lk.date_otvet}', "
                      f"planes='{json.dumps(lk.planes)}' "
                      f"WHERE id_lk={lk.id_lk}")
        query.exec(query_text)

    @staticmethod
    def delete_lk(lk: LK):
        query = QSqlQuery()
        query.exec(f"DELETE FROM lk WHERE id_lk={lk.id_lk}")

    def load_planes_by_podr(self, id_podr) -> list:
        result = []
        query = self.query_wp(f"SELECT * FROM planes WHERE id_podr={id_podr}")
        while query.next():
            plane = Plane()
            plane.unpack_plane(query.record())
            result.append(plane)
        return result

    def load_all_type(self) -> list:
        result = []
        query = self.load_all('planes_type')
        while query.next():
            type = Type()
            type.unpack_type(query.record())
            result.append(type)
        return result

    @staticmethod
    def add_spec(spec):
        query = QSqlQuery()
        query.exec(f"INSERT INTO spec VALUES(null, '{spec.name_spec}')")

    def update_spec(self, spec):
        self.query_wp("UPDATE spec SET name_spec=? WHERE id_spec=?", [spec.name_spec, spec.id_spec])

    def delete_spec(self, id_spec):
        self.query_wp("DELETE FROM spec WHERE id_spec=?", [id_spec])

    @staticmethod
    def add_podr(podr):
        query = QSqlQuery()
        query.exec(f"INSERT INTO podr VALUES(null, '{podr.name_podr}')")

    def update_podr(self, podr):
        self.query_wp("UPDATE podr SET name_podr=? WHERE id_podr=?", [podr.name_podr, podr.id_podr])

    def delete_podr(self, id_podr):
        self.query_wp("DELETE FROM podr WHERE id_podr=?", [id_podr])

    @staticmethod
    def add_type(type):
        query = QSqlQuery()
        query.exec(f"INSERT INTO planes_type VALUES(null, '{type.name_type}')")
        return

    def update_type(self, type):
        self.query_wp("UPDATE planes_type SET name_type=? WHERE id_type=?", [type.name_type, type.id_type])

    def delete_type(self, id_type):
        self.query_wp("DELETE FROM planes_type WHERE id_type=?", [id_type])

    def add_plane(self, plane: Plane):
        self.query_wp(
            "INSERT INTO planes (id_type, id_podr, bort_num, zav_num) VALUES(?, ?, ?, ?)",
            [plane.id_type, plane.id_podr, plane.bort_num, plane.zav_num])
        return

    def update_plane(self, plane: Plane):
        self.query_wp("UPDATE planes SET id_type=?, id_podr=?, bort_num=?, zav_num=? WHERE id_type=?",
                      [plane.id_type, plane.id_podr, plane.bort_num, plane.zav_num])

    def delete_plane(self, id_plane):
        self.query_wp("DELETE FROM planes WHERE id_plane=?", [id_plane])