from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkTagHandler import OkTagHandler
from OkScrollBar import OkScrollBar
import OkXmlHandler
from OkModel import OkModel
import re

class OkPreviewWidget(QtGui.QTextEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.cache = {}
        self.data = {}
        self.tag_position = {}
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #656565"
                "}")
        self.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        self.setVerticalScrollBar(OkScrollBar())
        
        okInfoDocument = QtGui.QTextDocument()
        self.cursor = QtGui.QTextCursor(okInfoDocument)
        self.cursor.setBlockFormat(OkBlockFormat())
        self.setDocument(okInfoDocument)
        
    def setupData(self, data):
        self.data = data
        for step in range(0, len(data)):
            self.titleFormat(step + 1)
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
            
            tp_sql = "INSERT INTO\n%s(%s)\n" % (step_data["table"], step_data["column"])
            self.contentFormat(tp_sql)
            self.subTag(data[step]["tags"], step_data["value"])
    
    @pyqtSlot(str, str, str)
    def tagValue(self, tag, text, type):
        for val in self.tag_position[tag]:
            ac_text = text
            block = self.document().findBlockByNumber(val[0])
            it = block.begin()
            it += (val[1] *2 + 1)
            fragment = it.fragment()
            self.cursor.setPosition(fragment.position())
            self.cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, fragment.length())
            self.cursor.deleteChar()
            if val[2] is not None:
                ac_text = OkTagHandler.callback(type + "_arg", ac_text, val[2])
            self.tagFormat(ac_text)
            
    def subTag(self, tags, data):
        self.cursor.insertText("VALUES( ", OkContentFormat())
        tag_pattern = r'\{[0-9a-zA-Z_]+\((?P<name>[0-9a-zA-Z_]+)\)\}'
        tag_compiler =re.compile(tag_pattern)
        tag_list = tag_compiler.split(data)
        order = 0
        arg_pattern = r'\{(?P<name>[0-9a-zA-Z_]+)(?:|\((?P<arg>[+-]{1}[0-9]+)\))\}'
        arg_compiler = re.compile(arg_pattern)
                
        for val in tag_list:
            if tags.get(val) is not None:
                arg_match = arg_compiler.match(tags[val])
                self.tag_position.setdefault(arg_match.group("name"), [])
                self.tag_position[arg_match.group("name")].append((self.cursor.blockNumber(), order, arg_match.group("arg")))
                self.tagFormat(tags[val])
                order += 1
            else:
                self.contentFormat(val)

        self.cursor.insertText(");\n", OkContentFormat())
        
    def titleFormat(self, step):
        self.cursor.insertText("/*Step %d */\n" % step, OkTitleFormat())
        
    def contentFormat(self, sql):
        self.cursor.insertText("%s" % sql, OkContentFormat())
        
    def tagFormat(self, tag):
        self.cursor.insertText("%s"% tag, OkTagFormat())
        
class OkBlockFormat(QtGui.QTextBlockFormat):
    def __init__(self):
        QtGui.QTextBlockFormat.__init__(self)
        self.setTopMargin(5)
        
class OkTitleFormat(QtGui.QTextCharFormat):
    def __init__(self):
        QtGui.QTextCharFormat.__init__(self)
        self.setFont(QtGui.QFont("微软雅黑", 8))

class OkContentFormat(QtGui.QTextCharFormat):
    def __init__(self):
        QtGui.QTextCharFormat.__init__(self)
        self.setFont(QtGui.QFont("微软雅黑", 9))
        
class OkTagFormat(QtGui.QTextCharFormat):
    def __init__(self):
        QtGui.QTextCharFormat.__init__(self)
        self.setFont(QtGui.QFont("微软雅黑", 12))
        self.setFontUnderline(True)
        tmpBrush = QtGui.QBrush(QtGui.QColor(255, 127, 102))
        self.setForeground(tmpBrush)
        
        
