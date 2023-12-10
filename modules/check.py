from dataclasses import dataclass
from PyQt6.QtSql import QSqlRecord
from main import AddCheck

@dataclass
class Check:
    id_check: str = ''
    name_check: str = ''
    period: str = ''
    last_check: str = ''

    def unpack_check(self, check:QSqlRecord):
        self.id_check = check.value('id_check')
        self.name_check = check.value('name_check')
        self.period = check.value('period')
        self.last_check = check.value('last_check')
        return self

    def pack_check(self, form: AddCheck):
        self.name_check = form.name_line_edit.text()
        self.period = form.period_combobox.currentText()
        self.last_check = form.last_check_date.date().toString('dd.MM.yyyy')
        return self

