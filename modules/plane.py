from dataclasses import dataclass
from PyQt6.QtSql import QSqlRecord

@dataclass
class Plane:
    id_plane: str = ''
    id_type: str = ''
    id_podr: str = ''
    bort_num: str = ''
    zav_num: str = ''
    temp_id_podr: str = ''

    def unpack_plane(self, record:QSqlRecord):
        self.id_plane = record.value('id_plane')
        self.id_podr = record.value('id_podr')
        self.id_type = record.value('id_type')
        self.zav_num = record.value('zav_num')
        self.bort_num = record.value('bort_num')
        self.temp_id_podr = record.value('temp_id_podr')
        return self
