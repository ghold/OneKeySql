import sys
from PyQt4 import QtGui
from MainWindow import MainWindow
import onekey_rc

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
