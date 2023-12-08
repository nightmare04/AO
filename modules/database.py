from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

from modules.spec import *
from modules.podr import *
from modules.plane import *
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
    def execute_query_with_params(sql_query, query_values=None):
        query = QSqlQuery()
        query.prepare(sql_query)
        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()
        return query

    def load_all(self, table) -> QSqlQuery:
        query_text = f"SELECT * FROM {table}"
        query = self.execute_query_with_params(query_text)
        return query

    def load_all_planes(self) -> list:
        result = []
        query = self.load_all('planes')
        while query.next():
            plane = Plane()
            plane.unpack_plane(query.record())
            result.append(plane)
        return result

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

    def load_all_spec(self) -> list:
        result = []
        query = self.load_all('spec')
        while query.next():
            spec = Spec()
            spec.unpack_spec(query.record())
            result.append(spec)
        return result

    def load_planes_by_podr(self, id_podr) -> list:
        result = []
        query = self.execute_query_with_params(f"SELECT * FROM planes WHERE id_podr={id_podr}")
        while query.next():
            plane = Plane()
            plane.unpack_plane(query.record())
            result.append(plane)
        return result

    @staticmethod
    def add_lk_to_db(data: LK):
        query = QSqlQuery()
        query.prepare("""INSERT into lk values (
                        null, :tlg, :date_tlg, :date_vypoln, :opisanie,
                        :lk, null, null, :komu_spec, :komu_planes, :complete)""")
        query.bindValue(':tlg', data.tlg)
        query.bindValue(':date_tlg', data.date_tlg)
        query.bindValue(':date_vypoln', data.date_vypoln)
        query.bindValue(':opisanie', data.opisanie)
        query.bindValue(':lk', data.lk)
        query.bindValue(':komu_spec', json.dumps(data.komu_spec))
        query.bindValue(':komu_planes', json.dumps(data.komu_planes))
        query.bindValue(':complete', 0)
        query.exec()

    @staticmethod
    def update_lk_in_db(lk: LK):
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
                      f"date_otvet='{lk.date_otvet}' "
                      f"WHERE id_lk={lk.id_lk}")
        query.exec(query_text)

    @staticmethod
    def delete_lk(lk: LK):
        query = QSqlQuery()
        query.exec(f"DELETE from lk WHERE id_lk={lk.id_lk}")
