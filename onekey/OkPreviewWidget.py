from PyQt4 import QtGui, QtCore, Qt
from OkScrollBar import OkScrollBar
import OkXmlHandler
from OkModel import OkModel

class OkPreviewWidget(QtGui.QTextEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.cache = {}
        self.data = {}
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #656565"
                "}")
        self.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        self.setVerticalScrollBar(OkScrollBar())
        
        okInfoDocument = QtGui.QTextDocument()
        self.cursor = QtGui.QTextCursor(okInfoDocument)
        self.cursor.setBlockFormat(OkBlockFormat())       
        self.cursor.insertText("helloworld\n", OkTitleFormat())
        self.cursor.endEditBlock()
        
        self.setDocument(okInfoDocument)
        
    def setupData(self, data):
        self.data = data
        for step in range(0, len(data)):
            self.stepNo(step + 1)
            key =  "%s_%s" %(data[step]["type"], data[step]["from"])
            model = self.cache.get(key)
            if  model is not None:
                pass
            else:
                xml_filename = "%s/%s.xml" % (data[step]["type"], data[step]["from"])
                handler_type = "Ok%sHandler" % data[step]["type"].capitalize()
                handler = getattr(OkXmlHandler, handler_type, None)
                model = OkModel(xml_filename, handler)
                self.cache[key] = model
                
            data_id = data[step]["type"] + "_" + data[step]["data_id"]
            step_data = model.data[data_id]["data"]
            sql = "INSERT INTO\n%s(%s)\nVALUES(%s);" % (step_data["table"], step_data["column"], step_data["value"])
            self.stepCon(sql)
            
    def stepNo(self, step):
        self.cursor.beginEditBlock()
        self.cursor.insertText("Step %d\n" % step, OkTitleFormat())
        self.cursor.endEditBlock()
        
    def stepCon(self, sql):
        self.cursor.beginEditBlock()
        self.cursor.insertText("%s\n" % sql, OkContentFormat())
        self.cursor.endEditBlock()
        
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
        
        
