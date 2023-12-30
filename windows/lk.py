from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QPushButton
from modules import DragGroupbox, DragButton
from ui import Ui_Add_lk_form
from datetime import datetime
from modules.database import *


class AddLk(QtWidgets.QWidget):
    def __init__(self, listk=ListControlM()):
        super().__init__()
        self.lk = listk
        self.spec_btns = []
        self.plane_type_btns = []
        self.unit_btns = []
        self.plane_btns = []
        self.plane_groups = []

        self.ui = Ui_Add_lk_form()
        self.ui.setupUi(self)
        self.ui.TlgDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.SrokDateEdit.setDate(QtCore.QDate().currentDate())
        self.ui.add_btn.clicked.connect(self.add_lk)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.fill_planes()
        self.fill_planes_to_unit()
        self.init_spec()
        self.setAcceptDrops(True)
        self.fill_selectors()

    def fill_selectors(self):
        main_groupbox = QGroupBox("Выбрать:")
        group_layout = QHBoxLayout()
        main_groupbox.setLayout(group_layout)
        self.ui.selectorLayout.addWidget(main_groupbox)

        unit_groupbox = QGroupBox("по подразделению:")
        group_layout.addWidget(unit_groupbox)
        unit_groupbox_layout = QGridLayout()
        unit_groupbox.setLayout(unit_groupbox_layout)
        units = UnitM.select()

        row = 0
        col = 0
        for unit in units:
            unit: UnitM
            btn = QPushButton(unit.name)
            btn.setCheckable(True)
            btn.clicked.connect(self.select_by_unit)
            btn.unit = unit
            self.unit_btns.append(btn)
            if btn.unit.performs_work:
                if col < 4:
                    unit_groupbox_layout.addWidget(btn, row, col)
                    col += 1
                else:
                    col = 0
                    row += 1
                    unit_groupbox_layout.addWidget(btn, row, col)
                    col += 1

        plane_type_groupbox = QGroupBox("по типу:")
        group_layout.addWidget(plane_type_groupbox)
        plane_type_groupbox_layout = QGridLayout()
        plane_type_groupbox.setLayout(plane_type_groupbox_layout)
        plane_types = PlaneTypeM.select()

        row = 0
        col = 0
        for pt in plane_types:
            pt: PlaneTypeM
            btn = QPushButton(pt.name)
            btn.setCheckable(True)
            btn.clicked.connect(self.select_by_plane_type)
            btn.plane_type = pt
            self.plane_type_btns.append(btn)
            if col < 4:
                plane_type_groupbox_layout.addWidget(btn, row, col)
                col += 1
            else:
                col = 0
                row += 1
                plane_type_groupbox_layout.addWidget(btn, row, col)
                col += 1

    def select_by_unit(self):

        for btn in self.plane_type_btns:
            btn.setChecked(False)

        btns = self.findChildren(DragButton)
        for unit_btn in self.unit_btns:
            for btn in btns:
                if btn.plane.id == unit_btn.unit.id and unit_btn.isChecked():
                    btn.setChecked(True)
                elif btn.plane.id == unit_btn.unit.id:
                    btn.setChecked(False)

    def select_by_plane_type(self):
        for btn in self.unit_btns:
            btn.setChecked(False)

        btns = self.findChildren(DragButton)
        for plane_type_btn in self.plane_type_btns:
            for btn in btns:
                if btn.plane.id == plane_type_btn.plane_type.id and plane_type_btn.isChecked():
                    btn.setChecked(True)
                elif btn.plane.id == plane_type_btn.plane_type.id:
                    btn.setChecked(False)

    def fill_planes(self):
        for pl in PlaneM.select():
            pl: PlaneM
            btn = DragButton(text=str(pl.tail_number))
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = pl
            self.plane_btns.append(btn)

    def fill_planes_to_unit(self):
        all_unit = UnitM.select()
        for u in all_unit:
            row = 0
            col = 0
            groupbox = DragGroupbox(u.name)
            layout_planes = QGridLayout()
            groupbox.setLayout(layout_planes)
            groupbox.unit = u
            groupbox.plane_btns = []
            self.ui.planesLayout.addWidget(groupbox)
            self.plane_groups.append(groupbox)
            for plane_btn in self.plane_btns:
                if plane_btn.plane.id == u.id:
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
                if plane_btn.plane.unit == groupbox.unit.id:
                    if col < 3:
                        groupbox.layout().addWidget(plane_btn, row, col)
                        col += 1
                    else:
                        col = 0
                        row += 1
                        groupbox.layout().addWidget(plane_btn, row, col)
                        col += 1
        for btn in self.plane_type_btns:
            if btn.isChecked():
                self.select_by_plane_type()

        for btn in self.unit_btns:
            if btn.isChecked():
                self.select_by_unit()

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
        all_spec = SubunitM.select()
        groupbox = QGroupBox("Специальности")
        layout_spec = QHBoxLayout()
        groupbox.setLayout(layout_spec)
        self.ui.SpecLayout.addWidget(groupbox)
        for s in all_spec:
            btn = QPushButton(s.name)
            btn.setCheckable(True)
            btn.spec = s
            self.spec_btns.append(btn)
            layout_spec.addWidget(btn)

    def add_lk(self):
        """Добавляем лист контроля в базу данных"""
        self.lk.telegram = self.ui.TlgLineEdit.text()
        self.lk.date_telegram = self.ui.TlgDateEdit.date().toPyDate()
        self.lk.date_deadline = self.ui.SrokDateEdit.date().toPyDate()
        self.lk.description = self.ui.textEdit.toPlainText()
        self.lk.number_lk = self.ui.LkLineEdit.text()
        self.lk.planes_for_exec = self.pack_planes_for_exec()
        self.lk.specialties_for_exec = self.pack_subunit_to_exec()
        self.lk.planes_on_create = self.pack_planes_on_create()
        self.lk.save()
        self.close()

    @staticmethod
    def pack_planes_on_create():
        result = []
        for plane in PlaneM.select():
            plane: PlaneM
            result.append({'id': str(plane.id),
                           'unit': str(plane.unit),
                           'plane_type': str(plane.plane_type),
                           'tail_number': str(plane.tail_number),
                           'factory_number': str(plane.factory_number)})

        return result

    def pack_planes_for_exec(self):
        planes_for_exec = []
        for plane_btn in self.plane_btns:
            if plane_btn.isChecked():
                planes_for_exec.append(plane_btn.plane.id)

        return planes_for_exec

    def pack_subunit_to_exec(self):
        subunit = []
        for subunit_btn in self.spec_btns:
            if subunit_btn.isChecked():
                subunit.append(subunit_btn.spec.id)

        return subunit


class EditLK(AddLk):
    def __init__(self, listk):
        super().__init__(listk)
        self.edit = True
        self.lk = listk
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle(f"Лист контроля №{self.lk.number_lk}")
        self.ui.add_btn.setText("Сохранить")
        self.ui.add_btn.clicked.disconnect()
        self.ui.add_btn.clicked.connect(self.save_lk)
        self.ui.cancel_btn.setText("Удалить")
        self.ui.cancel_btn.clicked.disconnect()
        self.ui.cancel_btn.clicked.connect(self.delete_lk)
        self.load_lk()
        self.update_planes()

    def fill_planes(self):
        for plane_from_lk in self.lk.planes_on_create:
            p = PlaneM(id=int(plane_from_lk['id']),
                       tail_number=plane_from_lk['tail_number'],
                       factory_number=plane_from_lk['factory_number'],
                       unit_id=plane_from_lk['unit'],
                       plane_type_id=plane_from_lk['plane_type'])

            btn = DragButton(text=p.tail_number)
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.plane = p
            self.plane_btns.append(btn)
            if p.id in self.lk.planes_for_exec:
                btn.setChecked(True)

    def load_lk(self):
        """Подгружаем лист контроля"""
        self.ui.TlgLineEdit.setText(self.lk.telegram)
        self.ui.TlgDateEdit.setDate(self.lk.date_telegram)
        self.ui.SrokDateEdit.setDate(self.lk.date_deadline)
        self.ui.textEdit.setText(self.lk.description)
        self.ui.LkLineEdit.setText(self.lk.number_lk)

        for spec_btn in self.spec_btns:
            spec_btn.setChecked(False)
            if spec_btn.spec.id in self.lk.specialties_for_exec:
                spec_btn.setChecked(True)

    def save_lk(self):
        self.add_lk()

    def delete_lk(self):
        self.lk.delete_instance()
        self.close()
