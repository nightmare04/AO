from PyQt6 import QtWidgets, QtGui
from windows import MainWindow
from modules import Database


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys

    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    main = MainWindow()
    sys.exit(app.exec())
