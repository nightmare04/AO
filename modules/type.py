from dataclasses import dataclass

from PyQt6.QtSql import QSqlRecord
from main import AddType


@dataclass
class Type:
    id_type: str = ''
    name_type: str = ''

    def unpack_type(self, record:QSqlRecord):
        self.id_type = record.value('id_type')
        self.name_type = record.value('name_type')
        return self

    def pack_type(self, form: AddType):
        self.id_type = form.type.id_type
        self.name_type = form.name_edit.text()
        return self
