from dataclasses import dataclass

from PyQt6.QtSql import QSqlRecord


@dataclass
class Podr:
    id_podr: str = ''
    name_podr: str = ''

    def unpack_podr(self, record:QSqlRecord):
        self.id_podr = record.value('id_podr')
        self.name_podr = record.value('name_podr')
        return self
