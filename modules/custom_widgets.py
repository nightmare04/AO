from PyQt6.QtWidgets import QPushButton, QGroupBox, QLabel
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap

class DragPlaneButton(QPushButton):
    def __init__(self, parent=None, text=None, icon=None, plane=None):
        super().__init__(parent=parent, text=text, icon=icon)
        self.plane = plane

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)


class DragGroupbox(QGroupBox):
    def __init__(self, text):
        super().__init__(text)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    # noinspection PyUnresolvedReferences
    def dropEvent(self, e):
        widget = e.source()
        widget.plane.unit = self.unit.id
        self.parent().update_planes()


class ClickQlabel(QLabel):
    clicked = pyqtSignal()

    # noinspection PyUnresolvedReferences
    def mousePressEvent(self, ev):
        self.clicked.emit()
        QLabel.mousePressEvent(self, ev)


class PlaneButton(QPushButton):
    def __init__(self, parent=None, text=None, icon=None, plane=None):
        super().__init__(parent=parent, text=text, icon=icon)
        self.plane = plane


class AgregateButton(QPushButton):
    def __init__(self, parent=None, text=None, icon=None, agr=None):
        super().__init__(parent=parent, text=text, icon=icon)
        self.agr = agr

