from dataclasses import dataclass

from PyQt6.QtSql import QSqlRecord
from main import AddPodr


@dataclass
class Podr:
    id_podr: str = ''
    name_podr: str = ''

    def unpack_podr(self, record: QSqlRecord):
        self.id_podr = str(record.value('id_podr'))
        self.name_podr = str(record.value('name_podr'))
        return self

    def pack_podr(self, form: AddPodr):
        self.id_podr = form.podr.id_podr
        self.name_podr = form.name_edit.text()
        return self
