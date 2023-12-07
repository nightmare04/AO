import json
from dataclasses import dataclass, field
from PyQt6.QtSql import QSqlRecord
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
        self.srok_tlg = record.value('date_vypoln')
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
        self.date_tlg = str(form.ui.TlgDateEdit.date().toPyDate())
        self.srok_tlg = str(form.ui.SrokDateEdit.date().toPyDate())
        self.lk = form.ui.LkLineEdit.text()
        self.komu_planes = self.pack_komu_planes(form)
        self.komu_spec = self.pack_komu_spec(form)

    @staticmethod
    def pack_komu_planes(form: AddLk) -> list:
        result = []
        for btn in form.plane_btns:
            if btn.isChecked():
                result.append(btn.plane.id_plane)
        return result

    @staticmethod
    def pack_komu_spec(form: AddLk) -> list:
        result = []
        for btn in form.spec_btns:
            if btn.isChecked():
                result.append(btn.spec.id_spec)
        return result
