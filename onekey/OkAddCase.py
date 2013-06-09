from PyQt4 import QtGui, QtCore, Qt

class OkAddCase(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.nameEdit = QtGui.QLineEdit(self)
        self.nameEdit.setPlaceholderText("名称")
        self.descEdit = OkTextEdit(self)
        
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.nameEdit)
        layout.addWidget(self.descEdit)
        
        self.setLayout(layout)
        
    def getNameAndDesc(self):
        if not self.descEdit.state:
            return (self.nameEdit.text(), self.descEdit.toPlainText())
        return (self.nameEdit.text(), '')
    
    def hideEvent(self, event):
        self.nameEdit.setText('')
        if not self.descEdit.state:
            self.descEdit.state = True
            self.descEdit.setTextColor(QtGui.QColor.fromRgb(128, 128, 128))
            self.descEdit.setText("描述")
            
        event.accept()
        
class OkTextEdit(QtGui.QTextEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.state = True
        self.setTextColor(QtGui.QColor.fromRgb(128, 128, 128))
        self.setText("描述")
        
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
            self.setTextColor(QtGui.QColor.fromRgb(128, 128, 128))
            self.setText("描述")
            event.accept() 
        QtGui.QTextEdit.focusOutEvent(self, event)
        event.accept()
