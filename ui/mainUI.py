# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setObjectName("main_layout")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.dolg_layout = QtWidgets.QVBoxLayout(self.groupBox)
        self.dolg_layout.setObjectName("dolg_layout")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.groupBox)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.dolg_layout.addWidget(self.tableWidget)
        self.add_btn = QtWidgets.QPushButton(parent=self.groupBox)
        self.add_btn.setObjectName("add_btn")
        self.dolg_layout.addWidget(self.add_btn)
        self.main_layout.addWidget(self.groupBox)
        self.checks_groupbox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.checks_groupbox.setFlat(True)
        self.checks_groupbox.setCheckable(False)
        self.checks_groupbox.setObjectName("checks_groupbox")
        self.main_layout.addWidget(self.checks_groupbox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_5.setObjectName("menu_5")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(parent=MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(parent=MainWindow)
        self.action_2.setObjectName("action_2")
        self.lk_action = QtGui.QAction(parent=MainWindow)
        self.lk_action.setObjectName("lk_action")
        self.podr_setup_action = QtGui.QAction(parent=MainWindow)
        self.podr_setup_action.setObjectName("podr_setup_action")
        self.spec_setup_action = QtGui.QAction(parent=MainWindow)
        self.spec_setup_action.setObjectName("spec_setup_action")
        self.plane_setup_action = QtGui.QAction(parent=MainWindow)
        self.plane_setup_action.setObjectName("plane_setup_action")
        self.types_setup_action = QtGui.QAction(parent=MainWindow)
        self.types_setup_action.setObjectName("types_setup_action")
        self.checks_setup_action = QtGui.QAction(parent=MainWindow)
        self.checks_setup_action.setObjectName("checks_setup_action")
        self.action_3 = QtGui.QAction(parent=MainWindow)
        self.action_3.setObjectName("action_3")
        self.system_action = QtGui.QAction(parent=MainWindow)
        self.system_action.setObjectName("system_action")
        self.action_5 = QtGui.QAction(parent=MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu_2.addAction(self.lk_action)
        self.menu_4.addAction(self.podr_setup_action)
        self.menu_4.addAction(self.types_setup_action)
        self.menu_4.addAction(self.plane_setup_action)
        self.menu_4.addAction(self.spec_setup_action)
        self.menu_4.addAction(self.checks_setup_action)
        self.menu_5.addAction(self.action_3)
        self.menu_5.addAction(self.system_action)
        self.menu_5.addAction(self.action_5)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Долги"))
        self.add_btn.setText(_translate("MainWindow", "Добавить"))
        self.checks_groupbox.setTitle(_translate("MainWindow", "Проверки"))
        self.menu.setTitle(_translate("MainWindow", "Файлы"))
        self.menu_2.setTitle(_translate("MainWindow", "Листы контроля"))
        self.menu_3.setTitle(_translate("MainWindow", "О программе"))
        self.menu_4.setTitle(_translate("MainWindow", "Настройки"))
        self.menu_5.setTitle(_translate("MainWindow", "Исправность"))
        self.action.setText(_translate("MainWindow", "Экспорт"))
        self.action_2.setText(_translate("MainWindow", "Настройки"))
        self.lk_action.setText(_translate("MainWindow", "Листы контроля"))
        self.podr_setup_action.setText(_translate("MainWindow", "Подразделения"))
        self.spec_setup_action.setText(_translate("MainWindow", "Специальности"))
        self.plane_setup_action.setText(_translate("MainWindow", "Самолеты"))
        self.types_setup_action.setText(_translate("MainWindow", "Типы самолетов"))
        self.checks_setup_action.setText(_translate("MainWindow", "Проверки"))
        self.action_3.setText(_translate("MainWindow", "Исправность"))
        self.system_action.setText(_translate("MainWindow", "Системы"))
        self.action_5.setText(_translate("MainWindow", "Блоки \\ Агрегаты"))
