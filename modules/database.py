import json

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

from modules.spec import *
from modules.podr import *
from modules.plane import *
from modules.type import *
from modules.lk import *
from modules.check import *


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
            lk = LK().unpack_lk(query.record())
            result.append(lk)
        return result

    def load_all_uncomplete_lk(self):
        result = []
        query_text = "SELECT * FROM lk WHERE complete=0"
        query = self.query_wp(query_text)
        while query.next():
            lk = LK().unpack_lk(query.record())
            result.append(lk)
        return result

    def load_all_podr(self) -> list:
        result = []
        query = self.load_all('podr')
        while query.next():
            podr = Podr().unpack_podr(query.record())
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
            spec = Spec().unpack_spec(query.record())
            result.append(spec)
        return result

    def load_plane(self, id_plane) -> Plane:
        query = self.query_wp("SELECT * FROM planes WHERE id_plane=?", [id_plane])
        query.next()
        return Plane().unpack_plane(query.record())

    def load_lk(self, id_lk) -> LK:
        query_text = f"SELECT * FROM lk WHERE id_lk={id_lk}"
        query = self.query_wp(query_text)
        query.first()
        return LK().unpack_lk(query.record())

    def add_lk(self, data: LK):
        query_text = ("INSERT INTO lk ("
                      "tlg, date_tlg, date_vypoln, opisanie, lk, "
                      "komu_spec, komu_planes, complete, planes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)")
        query_values = [
            data.tlg, data.date_tlg, data.date_vypoln,
            data.opisanie, data.lk, json.dumps(data.komu_spec),
            json.dumps(data.komu_planes), data.complete, json.dumps(data.planes)
        ]
        self.query_wp(query_text, query_values)

    def update_lk(self, lk: LK):

        query_text = ("UPDATE lk SET "
                      "tlg=?, date_tlg=?, date_vypoln=?, opisanie=?, "
                      "lk=?, komu_spec=?, komu_planes=?, complete=?, "
                      "otvet=?, date_otvet=?, planes=? WHERE id_lk=?")

        query_values = [
            lk.tlg, lk.date_tlg, lk.date_vypoln,
            lk.opisanie, lk.lk, json.dumps(lk.komu_spec),
            json.dumps(lk.komu_planes), lk.complete, lk.otvet,
            lk.date_otvet, json.dumps(lk.planes), lk.id_lk]

        self.query_wp(query_text, query_values)

    def delete_lk(self, lk: LK):
        self.query_wp("DELETE FROM lk WHERE id_lk=?", [lk.id_lk])
        self.query_wp("DELETE FROM lk_spec WHERE id_lk=?", [lk.id_lk])

    def load_all_type(self) -> list:
        result = []
        query = self.load_all('planes_type')
        while query.next():
            result.append(Type().unpack_type(query.record()))
        return result

    def add_spec(self, spec):
        self.query_wp(f"INSERT INTO spec (name_spec) VALUES(?)",
                      [spec.name_spec])

    def update_spec(self, spec):
        self.query_wp("UPDATE spec SET name_spec=? WHERE id_spec=?",
                      [spec.name_spec, spec.id_spec])

    def delete_spec(self, id_spec):
        self.query_wp("DELETE FROM spec WHERE id_spec=?", [id_spec])
        self.query_wp("DELETE FROM lk_compl WHERE id_spec=?", [id_spec])

    def add_podr(self, podr):
        self.query_wp("INSERT INTO podr (name_podr, with_planes) VALUES(?, ?)", [podr.name_podr, podr.with_planes])
        return

    def update_podr(self, podr):
        self.query_wp(
            "UPDATE podr SET name_podr=?, with_planes=? WHERE id_podr=?",
            [podr.name_podr, podr.with_planes, podr.id_podr])

    def delete_podr(self, id_podr):
        self.query_wp("DELETE FROM podr WHERE id_podr=?", [id_podr])
        self.query_wp("DELETE FROM plane WHERE id_podr=?", [id_podr])

    def add_type(self, t):
        self.query_wp("INSERT INTO planes_type (name_type) VALUES(?)", [t.name_type])

    def load_type_by_id(self, id_type) -> Type:
        query = self.query_wp(f"SELECT * FROM plane_types WHERE id_type={id_type}")
        query.first()
        return Type().unpack_type(query.record())

    def update_type(self, t):
        self.query_wp("UPDATE planes_type SET name_type=? WHERE id_type=?", [t.name_type, t.id_type])

    def delete_type(self, id_type):
        self.query_wp("DELETE FROM planes_type WHERE id_type=?", [id_type])
        self.query_wp("DELETE FROM planes WHERE id_type=?", [id_type])

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
        self.query_wp("DELETE FROM lk_compl WHERE id_plane=?", [id_plane])

    def add_complete(self, listk: LK, pl: Plane, spec: Spec):
        query_text = "INSERT INTO lk_compl (id_lk, id_plane, id_spec) VALUES(?, ?, ?)"
        query_values = [listk.id_lk, pl.id_plane, spec.id_spec]
        self.query_wp(query_text, query_values)

    def del_complete(self, listk: LK, pl: Plane, spec: Spec):
        query_text = "DELETE FROM lk_compl WHERE id_lk=? AND id_plane=? AND id_spec=?"
        query_values = [listk.id_lk, pl.id_plane, spec.id_spec]
        self.query_wp(query_text, query_values)

    def get_complete(self, listk: LK, pl: Plane) -> list:
        result = []
        query_text = "SELECT id_spec FROM lk_compl WHERE id_lk=? AND id_plane=?"
        query_values = [listk.id_lk, pl.id_plane]
        query = self.query_wp(query_text, query_values)
        while query.next():
            result.append(query.value(0))
        return result

    def get_not_done_planes(self, lk: LK):
        done = []
        not_done = []
        for id_plane in lk.komu_planes:
            plane = self.load_plane(id_plane)
            cmp = self.get_complete(lk, plane)
            if len(cmp) == len(lk.komu_spec):
                done.append(plane)
            else:
                not_done.append(plane)
        return done, not_done

    def add_check(self, check: Check):
        query_text = "INSERT INTO checks (name_check, period, last_check) VALUES(?, ?, ?)"
        query_values = [check.name_check, check.period, check.last_check]
        self.query_wp(query_text, query_values)

    def load_check(self, check: Check):
        query = self.query_wp(f"SELECT * FROM checks WHERE id_check={check.id_check}")
        query.first()
        return Check().unpack_check(query.record())

    def update_check(self, check: Check):
        query_text = "UPDATE checks SET name_check=?, period=?, last_check=? WHERE id_check=? VALUES(?, ?, ?, ?)"
        query_values = [check.name_check, check.period, check.last_check, check.id_check]
        self.query_wp(query_text, query_values)

    def load_all_checks(self):
        result = []
        query = self.query_wp(f"SELECT * FROM checks")
        while query.next():
            check = Check()
            check.unpack_check(query.record())
            result.append(check)
        return result

    def delete_check(self, check: Check):
        self.query_wp(f"DELETE FROM checks WHERE id_check={check.id_check}")
        self.query_wp(f"DELETE FROM checks_date WHERE id_check={check.id_check}")