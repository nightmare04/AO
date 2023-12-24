from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QPushButton
from modules import LK, DragGroupbox, DragButton
from ui import Ui_Add_lk_form
from datetime import datetime


class AddLk(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.lk = LK()
        self.db = db
        self.spec_btns = []
        self.type_btns = []
        self.podr_btns = []
        self.plane_btns = []
        self.plane_groups = []

        self.ui = Ui_Add_lk_form()
        self.ui.setupUi(self)
        self.ui.TlgDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.SrokDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.add_btn.clicked.connect(self.add_lk_to_db)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.fill_planes()
        self.fill_planes_to_podr()
        self.init_spec()
        self.setAcceptDrops(True)
        self.fill_selectors()

    def fill_selectors(self):
        main_groupbox = QGroupBox("Выбрать:")
        group_layout = QHBoxLayout()
        main_groupbox.setLayout(group_layout)
        self.ui.selectorLayout.addWidget(main_groupbox)

        podr_groupbox = QGroupBox("по подразделению:")
        group_layout.addWidget(podr_groupbox)
        podr_groupbox_layout = QGridLayout()
        podr_groupbox.setLayout(podr_groupbox_layout)
        podrs = self.db.load_all_podr()

        row = 0
        col = 0
        for pd in podrs:
            btn = QPushButton(pd.name_podr)
            btn.setCheckable(True)
            btn.clicked.connect(self.select_by_podr)
            btn.podr = pd
            self.podr_btns.append(btn)
            if btn.podr.with_planes:
                if col < 4:
                    podr_groupbox_layout.addWidget(btn, row, col)
                    col += 1
                else:
                    col = 0
                    row += 1
                    podr_groupbox_layout.addWidget(btn, row, col)
                    col += 1

        type_groupbox = QGroupBox("по типу:")
        group_layout.addWidget(type_groupbox)
        type_groupbox_layout = QGridLayout()
        type_groupbox.setLayout(type_groupbox_layout)
        types = self.db.load_all_type()

        row = 0
        col = 0
        for tp in types:
            btn = QPushButton(tp.name_type)
            btn.setCheckable(True)
            btn.clicked.connect(self.select_by_type)
            btn.type = tp
            self.type_btns.append(btn)
            if col < 4:
                type_groupbox_layout.addWidget(btn, row, col)
                col += 1
            else:
                col = 0
                row += 1
                type_groupbox_layout.addWidget(btn, row, col)
                col += 1

    def select_by_podr(self):

        for btn in self.type_btns:
            btn.setChecked(False)

        btns = self.findChildren(DragButton)
        for podr_btn in self.podr_btns:
            for btn in btns:
                if btn.plane.id_podr == podr_btn.podr.id_podr and podr_btn.isChecked():
                    btn.setChecked(True)
                elif btn.plane.id_podr == podr_btn.podr.id_podr:
                    btn.setChecked(False)

    def select_by_type(self):
        for btn in self.podr_btns:
            btn.setChecked(False)

        btns = self.findChildren(DragButton)
        for type_btn in self.type_btns:
            for btn in btns:
                if btn.plane.id_type == type_btn.type.id_type and type_btn.isChecked():
                    btn.setChecked(True)
                elif btn.plane.id_type == type_btn.type.id_type:
                    btn.setChecked(False)

    def fill_planes(self):
        for pl in self.db.load_all_planes():
            btn = DragButton(text=str(pl.bort_num))
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = pl
            self.plane_btns.append(btn)

    def fill_planes_to_podr(self):
        all_podr = self.db.load_all_podr()
        for p in all_podr:
            row = 0
            col = 0
            groupbox = DragGroupbox(p.name_podr)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.podr = p
            groupbox.plane_btns = []
            self.ui.planesLayout.addWidget(groupbox)
            self.plane_groups.append(groupbox)
            for plane_btn in self.plane_btns:
                if plane_btn.plane.id_podr == p.id_podr:
                    if col < 3:
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        row += 1
                        col = 0
                        layout_planes.addWidget(plane_btn, row, col)
                        col += 1

    def update_planes(self):
        for groupbox in self.plane_groups:
            layout = QGridLayout()
            groupbox.setLayout(layout)
            col = 0
            row = 0
            for plane_btn in self.plane_btns:
                if plane_btn.plane.id_podr == groupbox.podr.id_podr:
                    if col < 3:
                        groupbox.layout().addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        col = 0
                        row += 1
                        groupbox.layout().addWidget(plane_btn, row, col)
                        col += 1
        for btn in self.type_btns:
            if btn.isChecked():
                self.select_by_type()

        for btn in self.podr_btns:
            if btn.isChecked():
                self.select_by_podr()

    def check_toggle(self):
        """Проверка флага на подразделении"""
        sender = self.sender()
        for btn in sender.plane_btns:
            if sender.isChecked():
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def init_spec(self):
        """Готовим специальности"""
        all_spec = self.db.load_all_spec()
        groupbox = QGroupBox("Специальности")
        layout_spec = QHBoxLayout()
        groupbox.setLayout(layout_spec)
        self.ui.SpecLayout.addWidget(groupbox)
        for s in all_spec:
            btn = QPushButton(s.name_spec)
            btn.setCheckable(True)
            btn.spec = s
            self.spec_btns.append(btn)
            layout_spec.addWidget(btn)

    def add_lk_to_db(self):
        """Добавляем лист контроля в базу данных"""
        data = LK()
        data.pack_lk(self)
        self.db.add_lk(data)
        self.close()


class EditLK(AddLk):
    def __init__(self, listk, db):
        super().__init__(db)
        self.edit = True
        self.lk = listk
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle(f"Лист контроля №{self.lk.lk}")
        self.ui.add_btn.setText("Сохранить")
        self.ui.add_btn.clicked.disconnect()
        self.ui.add_btn.clicked.connect(self.save_lk)
        self.ui.cancel_btn.setText("Удалить")
        self.ui.cancel_btn.clicked.disconnect()
        self.ui.cancel_btn.clicked.connect(self.delete_lk)
        self.load_lk()
        self.fill_planes()
        self.update_planes()

    def fill_planes(self):
        for id_plane, id_podr in self.lk.planes.items():
            p = self.db.load_plane(id_plane)
            p.id_podr = id_podr
            btn = DragButton(text=str(p.bort_num))
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = p
            self.plane_btns.append(btn)

        for btn in self.plane_btns:
            if btn.plane.id_plane in self.lk.komu_planes:
                btn.setChecked(True)

    def load_lk(self):
        """Подгружаем лист контроля"""
        self.ui.TlgLineEdit.setText(self.lk.tlg)
        self.ui.TlgDateEdit.setDate(datetime.strptime(str(self.lk.date_tlg), '%d.%m.%Y'))
        self.ui.SrokDateEdit.setDate(datetime.strptime(str(self.lk.date_vypoln), '%d.%m.%Y'))
        self.ui.textEdit.setText(self.lk.opisanie)
        self.ui.LkLineEdit.setText(self.lk.lk)

        for plane_btn in self.plane_btns:
            plane_btn.setChecked(False)
            if plane_btn.plane.id_plane in self.lk.komu_planes:
                plane_btn.setChecked(True)

        for spec_btn in self.spec_btns:
            spec_btn.setChecked(False)
            if spec_btn.spec.id_spec in self.lk.komu_spec:
                spec_btn.setChecked(True)

    def save_lk(self):
        listk = LK()
        listk.pack_lk(self)
        self.db.update_lk(listk)
        self.close()

    def delete_lk(self):
        self.db.delete_lk(self.lk)
        self.close()
