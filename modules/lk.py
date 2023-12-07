import json
from dataclasses import dataclass, field

from PyQt6.QtSql import QSqlRecord
from PyQt6.QtWidgets import QPushButton, QGroupBox, QHBoxLayout
from PyQt6.QtCore import Qt

from main import AddLk


@dataclass
class LK:
    id_lk: str = ''
    tlg: str = ''
    date_tlg: str = ''
    srok_tlg: str = ''
    opisanie: str = ''
    lk: str = ''
    otvet: str = ''
    date_otvet: str = ''
    komu_planes: list = field(default_factory=list)
    komu_spec: list = field(default_factory=list)
    complete: int = 0

    def unpack_lk_from_db(self, record: QSqlRecord):
        self.id_lk = record.value('id_lk')
        self.tlg = record.value('tlg')
        self.date_tlg = record.value('date_tlg')
        self.srok_tlg = record.value('srok_tlg')
        self.opisanie = record.value('opisanie')
        self.lk = record.value('lk')
        self.otvet = record.value('otvet')
        self.date_otvet = record.value('date_otvet')
        self.komu_planes = json.loads(record.value('komu_planes'))
        self.komu_spec = json.loads(record.value('komu_spec'))
        self.complete = record.value('complete')
        return self

    def pack_lk_from_form(self, form: AddLk):
        self.opisanie = form.ui.textEdit.toPlainText()
        self.tlg = form.ui.TlgLineEdit.text()
        self.date_tlg = form.ui.TlgDateEdit.date().toString()
        self.srok_tlg = form.ui.SrokDateEdit.date().toString()
        self.lk = form.ui.LkLineEdit.text()
        self.komu_planes = self.pack_komu_planes(form)
        self.komu_spec = self.pack_komu_spec(form)

    def pack_komu_planes(self, form: AddLk) -> list:
        result = []
        for btn in form.plane_btns:
            if btn.isChecked():
                result.append(btn.plane.id_plane)
        return result

    def pack_komu_spec(self, form: AddLk) -> list:
        result = []
        for btn in form.spec_btns:
            if btn.isChecked():
                result.append(btn.spec.id_spec)
        return result
