from PyQt6 import QtWidgets, QtCore
from ui import Ui_CompleteForm
from docxtpl import DocxTemplate
from datetime import datetime
from modules import ListControlM, PlaneM, UnitM, CompleteLM, SubunitM
import os


class Complete(QtWidgets.QWidget):
    def __init__(self, listk):
        super().__init__()
        self.plane_complete = None
        self.lk = listk
        self.lk: ListControlM
        self.podrs = []
        self.plane_btns = []
        self.plane_groups = []
        self.ui = Ui_CompleteForm()
        self.ui.setupUi(self)

        self.ui.create_doc_btn.clicked.connect(self.create_doc)
        self.ui.save_btn.clicked.connect(self.save_lk)
        self.ui.cancel_btn.clicked.connect(self.close)

        self.ui.otvet_dateedit.setDate(QtCore.QDate().currentDate())
        self.setWindowTitle(f"Лист контроля №{str(self.lk.number_lk)}")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.init_planes()

    def init_planes(self):
        planes_for_exec = self.lk.planes_for_exec
        for plane in planes_for_exec:
            btn = QtWidgets.QPushButton()
            btn.plane = PlaneM.get(PlaneM.id == plane)
            btn.setText(btn.plane.tail_number)
            btn.setFixedWidth(40)
            btn.clicked.connect(self.open_plane_complete)
            btn.setChecked(True)
            self.plane_btns.append(btn)

        all_unit = UnitM.select()

        for unit in all_unit:
            groupbox = QtWidgets.QGroupBox(unit.name)
            layout_planes = QtWidgets.QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.podr = unit
            groupbox.plane_btns = []

            row = 0
            col = 0
            for plane_btn in self.plane_btns:
                if plane_btn.plane.unit.id == unit.id:
                    if col < 3:
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        row += 1
                        col = 0
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1

                self.ui.podr_layout.addWidget(groupbox)
                self.plane_groups.append(groupbox)

        self.ui.complete_checkbox.setChecked(self.lk.complete_flag)
        self.ui.otvet_linedit.setText(self.lk.answer)
        if self.lk.answer_date:
            self.ui.otvet_dateedit.setDate(self.lk.answer_date)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.check_complete()
        return QtWidgets.QWidget.event(self, e)

    def check_complete(self):
        for btn in self.plane_btns:
            count = (CompleteLM.select().
                     where(CompleteLM.id_plane == btn.plane.id).
                     where(CompleteLM.id_list == self.lk.id))
            if len(count) == len(self.lk.specialties_for_exec):
                btn.setStyleSheet("background-color: green; color: white;")

            else:
                btn.setStyleSheet("background-color: red; color: white;")

    def create_doc(self):
        context = {
            'tlg': str(self.lk.telegram),
            'date_tlg': str(self.lk.date_telegram.strftime("%d.%m.%Y")),
            'lk': str(self.lk.number_lk),
            'today': datetime.today().strftime("%d.%m.%Y")
        }

        doc = DocxTemplate("templates/Телеграмма.docx")
        doc.render(context)
        doc.save("templates/out.docx")
        os.system("start templates/out.docx")
        self.close()

    def save_lk(self):
        if self.ui.complete_checkbox.isChecked():
            self.lk.complete = 1
        if not self.ui.otvet_linedit.text() == "":
            self.lk.otvet = self.ui.otvet_linedit.text()
            self.lk.date_otvet = self.ui.otvet_dateedit.date().toString('dd.MM.yyyy')
        self.db.update_lk(self.lk)
        self.close()

    def open_plane_complete(self):
        sender = self.sender()
        self.plane_complete = EditComplete(sender.plane, self.lk)
        self.plane_complete.show()


class EditComplete(QtWidgets.QWidget):
    def __init__(self, plane, listk, parent=None):
        super().__init__(parent)
        self.lk = listk
        self.plane = plane
        self.resize(250, 200)
        self.setWindowTitle(f'Самолет №{self.plane.tail_number}')
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.subunits = SubunitM.select()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.completed = self.compl_from_model()
        self.init_subunits()

    def init_subunits(self):
        for su in self.subunits:
            btn = QtWidgets.QPushButton(su.name)
            btn.spec = su
            btn.setCheckable(True)
            btn.lk = self.lk
            btn.clicked.connect(self.handle_spec)
            if btn.spec.id in btn.lk.specialties_for_exec:
                self.main_layout.addWidget(btn)
                if str(btn.spec.id) in self.completed:
                    btn.setChecked(True)

    def compl_from_model(self):
        result = []
        for model in CompleteLM.select().where(CompleteLM.id_plane == self.plane.id, CompleteLM.id_list == self.lk.id):
            result.append(str(model.id_subunit))
        return result

    def handle_spec(self):
        sender = self.sender()
        if sender.isChecked():
            CompleteLM.create(id_list=self.lk.id, id_plane=self.plane.id, id_subunit=sender.spec.id)
        else:
            compl = CompleteLM.get(id_list=self.lk.id, id_plane=self.plane.id, id_subunit=sender.spec.id)
            compl.delete_instance()
            
