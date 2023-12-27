from PyQt6 import QtWidgets, QtCore
from ui import Ui_CompleteForm
from docxtpl import DocxTemplate
from datetime import datetime
from modules import ListControlModel, PlaneModel, UnitModel
import os


class Complete(QtWidgets.QWidget):
    def __init__(self, listk):
        super().__init__()
        self.plane_complete = None
        self.lk = listk
        self.lk: ListControlModel
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
        for id_plane, id_podr in PlaneModel.select(ListControlModel.planes_for_exec).items():
            pl = PlaneModel.get(PlaneModel.id == id_plane)
            pl.unit = id_podr
            btn = QtWidgets.QPushButton(str(pl.tail_number))
            btn.setFixedWidth(40)
            btn.plane = pl
            btn.clicked.connect(self.open_plane_complete)
            btn.setChecked(True)
            self.plane_btns.append(btn)

        all_unit = UnitModel.select()
        for u in all_unit:
            groupbox = QtWidgets.QGroupBox(u.name)
            layout_planes = QtWidgets.QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.podr = u
            groupbox.plane_btns = []

            row = 0
            col = 0
            for plane_btn in self.plane_btns:
                if (plane_btn.plane.id in self.lk.planes_for_exec) and (plane_btn.plane.id_podr == u.id_podr):
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

        self.ui.complete_checkbox.setChecked(bool(self.lk.complete))
        self.ui.otvet_linedit.setText(self.lk.otvet)
        if not self.lk.date_otvet == '':
            self.ui.otvet_dateedit.setDate(datetime.strptime(str(self.lk.date_otvet), '%d.%m.%Y'))

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self.check_complete()
        return QtWidgets.QWidget.event(self, e)

    def check_complete(self):
        for btn in self.plane_btns:
            if len(self.db.get_complete(self.lk, btn.plane)) == len(self.lk.komu_spec):
                btn.setStyleSheet("background-color: green; color: white;")

            else:
                btn.setStyleSheet("background-color: red; color: white;")

    def create_doc(self):
        context = {
            'tlg': str(self.lk.tlg),
            'date_tlg': str(self.lk.date_tlg),
            'lk': str(self.lk.lk),
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
        self.plane_complete = EditComplete(sender.plane, self.lk, self.db)
        self.plane_complete.show()


class EditComplete(QtWidgets.QWidget):
    def __init__(self, pl, listk, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.compl = self.db.get_complete(listk, pl)
        self.lk = listk
        self.plane = pl
        self.resize(250, 200)
        self.setWindowTitle(f'Самолет №{self.plane.bort_num}')
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.specs = self.db.load_all_spec()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        for sp in self.specs:
            btn = QtWidgets.QPushButton(sp.name_spec)
            btn.spec = sp
            btn.setCheckable(True)
            btn.lk = self.lk
            btn.clicked.connect(self.handle_spec)
            if btn.spec.id_spec in btn.lk.komu_spec:
                self.main_layout.addWidget(btn)
                if int(btn.spec.id_spec) in self.compl:
                    btn.setChecked(True)

    def handle_spec(self):
        sender = self.sender()
        if sender.isChecked():
            self.db.add_complete(self.lk, self.plane, sender.spec)
        else:
            self.db.del_complete(self.lk, self.plane, sender.spec)
            
