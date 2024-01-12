from PyQt6 import QtWidgets, QtGui

from modules.database import create_tables
from windows import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys
    create_tables()
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    main = MainWindow()
    sys.exit(app.exec())
