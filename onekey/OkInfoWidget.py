from PyQt4 import  Qt

class OkInfoWidget(Qt.QTextEdit):
    def __init__(self, parent=None):
        Qt.QTextEdit.__init__(self, parent)
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #eeeeee"
                "}")
        self.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        
        okInfoDocument = Qt.QTextDocument()
        self.cursor = Qt.QTextCursor(okInfoDocument)
        self.setDocument(okInfoDocument)
        
    def infoGeneratorUTF8(self, item):
        data = item.data(0, Qt.Qt.UserRole)
        self.document().clear()
        self.cursor.setBlockFormat(OkBlockFormat())
        self.cursor.insertText("%s-%s\n"%(data['id'], data['data']['name']), OkTitleFormat())
        self.cursor.insertText("%s\n"%data['data']['desc'], OkContentFormat())
        
class OkBlockFormat(Qt.QTextBlockFormat):
    def __init__(self):
        Qt.QTextBlockFormat.__init__(self)
        self.setTopMargin(20)
        
class OkTitleFormat(Qt.QTextCharFormat):
    def __init__(self):
        Qt.QTextCharFormat.__init__(self)
        self.setFont(Qt.QFont("微软雅黑", 16))

class OkContentFormat(Qt.QTextCharFormat):
    def __init__(self):
        Qt.QTextCharFormat.__init__(self)
        self.setFont(Qt.QFont("微软雅黑", 12))
        
class OkTagFormat(Qt.QTextCharFormat):
    def __init__(self):
        Qt.QTextCharFormat.__init__(self)
        self.setFont(Qt.QFont("微软雅黑", 12))
        
        
