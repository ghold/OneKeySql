from PyQt4 import QtGui, QtCore, Qt

class OkAddCase(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        nameEdit = QtGui.QLineEdit()
        nameEdit.setPlaceholderText("名称")
        descEdit = OkTextEdit()
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(nameEdit)
        layout.addWidget(descEdit)
        
        self.setLayout(layout)
        
class OkTextEdit(QtGui.QTextEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.state = True
        self.setText("描述")
        self.setTextColor(QtGui.QColor.fromRgb(128, 128, 128))
        
    def focusInEvent(self, event):
        if self.state:
            self.clear()
            self.state = False
            self.setTextColor(QtGui.QColor.fromRgb(0, 0, 0))
            event.accept()
        QtGui.QTextEdit.focusInEvent(self, event)
        event.accept()
    
    def focusOutEvent(self, event):
        if not self.state and len(self.toPlainText()) == 0:
            self.state = True
            self.setText("描述")
            self.setTextColor(QtGui.QColor.fromRgb(226, 226, 226))
            event.accept() 
        QtGui.QTextEdit.focusOutEvent(self, event)
        event.accept()
