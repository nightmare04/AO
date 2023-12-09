from dataclasses import dataclass
from PyQt6.QtSql import QSqlRecord
from main import AddPlane


@dataclass
class Plane:
    id_plane: str = ''
    id_type: str = ''
    id_podr: str = ''
    bort_num: str = ''
    zav_num: str = ''

    def unpack_plane(self, record: QSqlRecord):
        self.id_plane = str(record.value('id_plane'))
        self.id_podr = str(record.value('id_podr'))
        self.id_type = str(record.value('id_type'))
        self.zav_num = str(record.value('zav_num'))
        self.bort_num = str(record.value('bort_num'))
        return self

    def pack_plane(self, form: AddPlane):
        self.id_plane = form.plane.id_plane
        self.id_podr = form.podrs[form.podr_select.currentText()]
        self.id_type = form.types[form.type_select.currentText()]
        self.zav_num = form.zav_num_edit.text()
        self.bort_num = form.bort_num_edit.text()
        return self
