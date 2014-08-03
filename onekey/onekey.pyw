import sys
from PyQt4 import Qt
import MainWindow
import onekey_rc

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    main_window = MainWindow.MainWindow()
    main_window.show()
    sys.exit(app.exec_())
