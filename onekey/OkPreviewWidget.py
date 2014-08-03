from PyQt4 import Qt, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkTagHandler import OkTagHandler
from OkScroll import OkScrollBar
import OkXmlHandler
from OkModel import OkModel
from OkConfig import OkConfig
import re

class OkPreviewWidget(Qt.QTextEdit):
    def __init__(self, parent=None):
        Qt.QTextEdit.__init__(self, parent)
        self.cache = {}
        self.data = {}
        self.tag_position = {}
        self.config = OkConfig()
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #656565"
                "}")
        #self.setMaximumHeight(600)
        self.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.MinimumExpanding)
        self.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        self.setVerticalScrollBar(OkScrollBar())
        
        okInfoDocument = Qt.QTextDocument()
        self.cursor = Qt.QTextCursor(okInfoDocument)
        self.cursor.setBlockFormat(OkBlockFormat())
        self.setDocument(okInfoDocument)
        
    def setupData(self, data):
        self.data = data
        for step in range(0, len(data)):
            
            key =  "%s_%s" %(data[step]["type"], data[step]["from"])
            model = self.cache.get(key)
            
            if  model is not None:
                pass
            else:
                xml_filename = "%s/%s.xml" % (data[step]["type"], data[step]["from"])
                handler_type = "Ok%sHandler" % data[step]["type"].capitalize()
                handler = getattr(OkXmlHandler, handler_type, None)
                model = OkModel((xml_filename, handler, 'unit'))
                self.cache[key] = model
            
            data_id = data[step]["type"] + "_" + data[step]["data_id"]
            step_data = model.data['unit'][data_id]["data"]
            
            self.titleFormat(step + 1, step_data['desc'])
            
            if (step_data.get("table", None) is not None and step_data.get("column", None) is not None):
                tp_sql = "INSERT INTO\n%s(%s)\n" % (step_data["table"], step_data["column"])
                self.contentFormat(tp_sql)
                self.subTag(data[step]["tags"], step_data["value"], False)
            else:
                self.subTag(data[step]["tags"], step_data["value"], True)
        self.cursor.movePosition(Qt.QTextCursor.Start)
    
    @pyqtSlot(str, str, str, str)
    def tagValue(self, tag, text, type, default):
        self.config.reset()
        for val in self.tag_position[tag]:
            ac_text = text
            block = self.document().findBlockByNumber(val[0])
            it = block.begin()
            it += (val[1] *2 + 1)
            fragment = it.fragment()
            self.cursor.setPosition(fragment.position())
            self.cursor.movePosition(Qt.QTextCursor.Right, Qt.QTextCursor.KeepAnchor, fragment.length())
            self.cursor.deleteChar()
            #if arg is set, it will be call the "_arg" suffix method
            if val[2] is not None:
                if val[2] != 'repeat':
                    ac_text = OkTagHandler.callback(type + "_arg", ac_text, val[2], default, self.config)
                else:
                    ac_text = OkTagHandler.callback("repeat_arg", ac_text, val[2], default, self.config)
                    val_new = (val[0],val[1],None)
                    self.tag_position[tag].remove(val)
                    self.tag_position[tag].insert(0, val_new)
            self.tagFormat(ac_text)
        
    def subTag(self, tags, data, spec):
        if spec:
            pass
        else:
            self.cursor.insertText("VALUES( ", OkContentFormat())
        tag_pattern = r'\{[0-9a-zA-Z_@%]+\((?P<name>(?:[@%]|)[0-9a-zA-Z_]+)\)\}'
        tag_compiler =re.compile(tag_pattern)
        tag_list = tag_compiler.split(data)
        order = 0
        arg_pattern = r'\{(?P<name>[0-9a-zA-Z_]+)(?:|\((?P<arg>[+-]{1}[0-9]+)\))\}'
        arg_compiler = re.compile(arg_pattern)
        for val in tag_list:
            if tags.get(val) is not None:
                arg_match = arg_compiler.match(tags[val])
                if arg_match is not None:
                    self.tag_position.setdefault(arg_match.group("name"), [])
                    self.tag_position[arg_match.group("name")].append((self.cursor.blockNumber(), order, arg_match.group("arg")))
                self.tagFormat(tags[val])
                order += 1
            elif val[0:1] and tags.get(val[1:]) is not None:
                arg_match = arg_compiler.match(tags[val[1:]])
                if arg_match is not None and val[0:1] == '%':
                    self.tag_position.setdefault(arg_match.group("name"), [])
                    self.tag_position[arg_match.group("name")].append((self.cursor.blockNumber(), order, 'repeat'))
                elif arg_match is not None and val[0:1] == '@':
                    val_idx = len(self.tag_position[arg_match.group("name")])
                    if val_idx == 0:
                        continue
                    else:
                        self.tag_position[arg_match.group("name")].append((self.cursor.blockNumber(), order,self.tag_position[arg_match.group("name")][val_idx-1][2]))

                self.tagFormat(tags[val[1:]])
                order += 1
            else:
                self.contentFormat(val)
                
        if spec:
            self.cursor.insertText(";\n", OkContentFormat())
        else:
            self.cursor.insertText(");\n", OkContentFormat())
        
    def titleFormat(self, step, desc):
        self.cursor.insertText("/*Step %d：%s*/\n" % (step, desc), OkTitleFormat())
        
    def contentFormat(self, sql):
        self.cursor.insertText("%s" % sql, OkContentFormat())
        
    def tagFormat(self, tag):
        self.cursor.insertText("%s"% tag, OkTagFormat())
        
class OkBlockFormat(Qt.QTextBlockFormat):
    def __init__(self):
        Qt.QTextBlockFormat.__init__(self)
        self.setTopMargin(5)
        
class OkTitleFormat(Qt.QTextCharFormat):
    def __init__(self):
        Qt.QTextCharFormat.__init__(self)
        self.setFont(Qt.QFont("微软雅黑", 8))

class OkContentFormat(Qt.QTextCharFormat):
    def __init__(self):
        Qt.QTextCharFormat.__init__(self)
        self.setFont(Qt.QFont("微软雅黑", 9))
        
class OkTagFormat(Qt.QTextCharFormat):
    def __init__(self):
        Qt.QTextCharFormat.__init__(self)
        self.setFont(Qt.QFont("微软雅黑", 12))
        self.setFontUnderline(True)
        tmpBrush = Qt.QBrush(Qt.QColor(255, 127, 102))
        self.setForeground(tmpBrush)
        
        
