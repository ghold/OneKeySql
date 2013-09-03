from PyQt4 import QtGui, QtCore, Qt

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
        self.setDocument(okInfoDocument)
        
    def infoGeneratorUTF8(self, item):
        data = item.data(0, Qt.Qt.UserRole)
        self.document().clear()
        self.cursor.setBlockFormat(OkBlockFormat())
        self.cursor.insertText("%s-%s\n"%(data['id'], data['data']['name']), OkTitleFormat())
        self.cursor.insertText("%s\n"%data['data']['desc'], OkContentFormat())
        
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
        
        
