from PyQt4 import Qt, QtCore

class OkAddCase(Qt.QWidget):
    def __init__(self, parent=None):
        Qt.QWidget.__init__(self, parent)
        
        self.nameEdit = Qt.QLineEdit(self)
        self.nameEdit.setPlaceholderText("名称")
        self.cateEdit = Qt.QLineEdit(self)
        self.cateEdit.setPlaceholderText("分类")
        self.descEdit = OkTextEdit(self)
        
        layout = Qt.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.nameEdit)
        layout.addWidget(self.cateEdit)
        layout.addWidget(self.descEdit)
        
        self.setLayout(layout)
        
    def getNameAndDesc(self):
        if not self.descEdit.state:
            return (self.nameEdit.text(), self.cateEdit.text(), self.descEdit.toPlainText())
        return (self.nameEdit.text(), self.cateEdit.text(), '')
    
    def hideEvent(self, event):
        self.nameEdit.setText('')
        self.cateEdit.setText('')
        if not self.descEdit.state:
            self.descEdit.state = True
            self.descEdit.setTextColor(Qt.QColor.fromRgb(128, 128, 128))
            self.descEdit.setText("描述")
            
        event.accept()
        
class OkTextEdit(Qt.QTextEdit):
    def __init__(self, parent=None):
        Qt.QTextEdit.__init__(self, parent)
        self.state = True
        self.setTextColor(Qt.QColor.fromRgb(128, 128, 128))
        self.setText("描述")
        
    def focusInEvent(self, event):
        if self.state:
            self.clear()
            self.state = False
            self.setTextColor(Qt.QColor.fromRgb(0, 0, 0))
            event.accept()
        Qt.QTextEdit.focusInEvent(self, event)
        event.accept()
    
    def focusOutEvent(self, event):
        if not self.state and len(self.toPlainText()) == 0:
            self.state = True
            self.setTextColor(Qt.QColor.fromRgb(128, 128, 128))
            self.setText("描述")
            event.accept() 
        Qt.QTextEdit.focusOutEvent(self, event)
        event.accept()
