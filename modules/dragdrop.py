from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QGroupBox
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap


class DragButton(QPushButton):

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

    def dropEvent(self, e):
        widget = e.source()
        widget.plane.id_podr = self.podr.id_podr
        self.parent().update_planes()
