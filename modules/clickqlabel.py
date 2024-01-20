from PyQt6 import QtWidgets, QtCore

class ClickQlabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, ev)
