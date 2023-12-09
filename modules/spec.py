from dataclasses import dataclass
from PyQt6.QtSql import QSqlRecord
from main import AddSpec

@dataclass
class Spec:
    id_spec: str = ''
    name_spec: str = ''

    def unpack_spec(self, record: QSqlRecord):
        self.id_spec = str(record.value('id_spec'))
        self.name_spec = str(record.value('name_spec'))
        return self

    def pack_spec(self, form: AddSpec):
        self.id_spec = form.spec.id_spec
        self.name_spec = form.name_edit.text()
        return self
