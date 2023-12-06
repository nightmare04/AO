from dataclasses import dataclass
from PyQt6.QtSql import QSqlRecord


@dataclass
class Spec:
    id_spec: str = ''
    name_spec: str = ''

    def unpack_podr(self, record:QSqlRecord):
        self.id_spec = record.value('id_spec')
        self.name_spec = record.value('name_spec')
        return self
