from dataclasses import dataclass

from PyQt6.QtSql import QSqlRecord



@dataclass
class Podr:
    id_podr: str = ''
    name_podr: str = ''
    with_planes: int = 0

    def unpack_podr(self, record: QSqlRecord):
        self.id_podr = str(record.value('id_podr'))
        self.name_podr = str(record.value('name_podr'))
        self.with_planes = record.value('with_planes')
        return self

    def pack_podr(self, form):
        self.id_podr = form.podr.id_podr
        self.name_podr = form.name_edit.text()
        self.with_planes = int(form.with_planes.isChecked())
        return self
