from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkListItem import OkListItem

class OkInfoWidget(QtGui.QTextEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #eeeeee"
                "}")
        self.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        
        okInfoDocument = QtGui.QTextDocument()
        self.cursor = QtGui.QTextCursor(okInfoDocument)
        self.cursor.setBlockFormat(OkBlockFormat())
        self.cursor.beginEditBlock()
        self.cursor.insertText("helloworld\n", OkTitleFormat())
        self.cursor.endEditBlock()
        self.cursor.beginEditBlock()
        self.cursor.insertText("Python 3.3.1 (v3.3.1:d9893d13c628, Apr  6 2013, 20:30:21) [MSC v.1600 64 bit (AMD64)] on Ghold-PC, Standard\n", OkContentFormat())
        self.cursor.endEditBlock()
        self.cursor.beginEditBlock()
        self.cursor.insertText("helloworld\n", OkTitleFormat())
        self.cursor.endEditBlock()
        
        self.setDocument(okInfoDocument)
        
    @pyqtSlot(OkListItem)
    def infoGeneratorUTF8(self, item):
        self.cursor.insertText(item.data(Qt.Qt.UserRole)['id'], OkContentFormat())
        
class OkBlockFormat(QtGui.QTextBlockFormat):
    def __init__(self):
        QtGui.QTextBlockFormat.__init__(self)
        self.setTopMargin(20)
        
class OkTitleFormat(QtGui.QTextCharFormat):
    def __init__(self):
        QtGui.QTextCharFormat.__init__(self)
        self.setFont(QtGui.QFont("微软雅黑", 16))

class OkContentFormat(QtGui.QTextCharFormat):
    def __init__(self):
        QtGui.QTextCharFormat.__init__(self)
        self.setFont(QtGui.QFont("微软雅黑", 12))
        
class OkTagFormat(QtGui.QTextCharFormat):
    def __init__(self):
        QtGui.QTextCharFormat.__init__(self)
        self.setFont(QtGui.QFont("微软雅黑", 12))
        
        
