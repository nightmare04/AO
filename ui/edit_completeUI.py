# Form implementation generated from reading ui file '.\ui\edit_complete.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_CompleteForm(object):
    def setupUi(self, CompleteForm):
        CompleteForm.setObjectName("CompleteForm")
        CompleteForm.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        CompleteForm.resize(442, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(CompleteForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.podr_layout = QtWidgets.QHBoxLayout()
        self.podr_layout.setObjectName("podr_layout")
        self.verticalLayout.addLayout(self.podr_layout)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        self.save_btn = QtWidgets.QPushButton(parent=CompleteForm)
        self.save_btn.setObjectName("save_btn")
        self.buttons_layout.addWidget(self.save_btn)
        self.cancel_btn = QtWidgets.QPushButton(parent=CompleteForm)
        self.cancel_btn.setObjectName("cancel_btn")
        self.buttons_layout.addWidget(self.cancel_btn)
        self.create_doc_btn = QtWidgets.QPushButton(parent=CompleteForm)
        self.create_doc_btn.setObjectName("create_doc_btn")
        self.buttons_layout.addWidget(self.create_doc_btn)
        self.complete_checkbox = QtWidgets.QCheckBox(parent=CompleteForm)
        self.complete_checkbox.setObjectName("complete_checkbox")
        self.buttons_layout.addWidget(self.complete_checkbox)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.otvet_label = QtWidgets.QLabel(parent=CompleteForm)
        self.otvet_label.setObjectName("otvet_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.otvet_label)
        self.otvet_linedit = QtWidgets.QLineEdit(parent=CompleteForm)
        self.otvet_linedit.setObjectName("otvet_linedit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.otvet_linedit)
        self.otvet_date_label = QtWidgets.QLabel(parent=CompleteForm)
        self.otvet_date_label.setObjectName("otvet_date_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.otvet_date_label)
        self.otvet_dateedit = QtWidgets.QDateEdit(parent=CompleteForm)
        self.otvet_dateedit.setCalendarPopup(True)
        self.otvet_dateedit.setObjectName("otvet_dateedit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.otvet_dateedit)
        self.buttons_layout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.buttons_layout)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(CompleteForm)
        QtCore.QMetaObject.connectSlotsByName(CompleteForm)

    def retranslateUi(self, CompleteForm):
        _translate = QtCore.QCoreApplication.translate
        CompleteForm.setWindowTitle(_translate("CompleteForm", "Лист контроля"))
        self.save_btn.setText(_translate("CompleteForm", "Сохранить"))
        self.cancel_btn.setText(_translate("CompleteForm", "Отменить"))
        self.create_doc_btn.setText(_translate("CompleteForm", "Ответить"))
        self.complete_checkbox.setText(_translate("CompleteForm", "Выполнено"))
        self.otvet_label.setText(_translate("CompleteForm", "Ответ ТЛГ"))
        self.otvet_date_label.setText(_translate("CompleteForm", "Дата ответа"))
