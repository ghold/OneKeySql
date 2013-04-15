from PyQt4 import QtGui, Qt
from ui_previewer import Ui_Form

class MainWindow(QtGui.QWidget,  Ui_Form):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        #self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        
        self.setupUi(self)
        
    def exit(self):
        self.close()
