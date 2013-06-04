from PyQt4 import QtGui, QtCore, Qt
from OkToolBar import OkEditToolBar
from OkLabel import OkEditWidgetLabel
from OkButton import OkExecButton
from OkTagSetting import OkTagSetting
from OkTagBox import OkTagBox
import re

class OkCaseEditPad(QtGui.QWidget):
    editWidget = None
    caseData = {}
    insertData = {}
    def __init__(self, casedata, insertdata, parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(200, 0, self.parent().width() - 200 ,  self.parent().height()))
        self.caseData = casedata
        self.insertData = insertdata
        #add toolBar
        self.toolBar = OkEditToolBar(self)
        
        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        verticalSpacer = QtGui.QSpacerItem(20, 30)
        #tag
        tagLabel = OkEditWidgetLabel("标签")
        self.tagWidget = OkTagBox(self.setupTag(), self)
        settingLabel = OkEditWidgetLabel("设置")
        
        #add layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        editLayout = QtGui.QVBoxLayout()
        
        #setting layout
        settingWidget = self.setupLabel()
        #comfireButton
        self.comfirmButton = OkExecButton("保存")
        #self.comfirmButton.clicked.connect(self.sqlExec)
        #
        horizonLayout = QtGui.QHBoxLayout()
        horizonLayout.addWidget(settingLabel)
        horizonLayout.addWidget(self.comfirmButton )
        
        # add the widgets.
        editLayout.addWidget(tagLabel, 0, Qt.Qt.AlignTop)
        editLayout.addWidget(self.tagWidget, 0, Qt.Qt.AlignTop)
        editLayout.addLayout(horizonLayout, 0)
        if settingWidget is not None:
            editLayout.addWidget(settingWidget, 1)
        
        gridLayout.addLayout(editLayout, 1, 1)
        
        self.setLayout(gridLayout)
        
    def setupTag(self):
        tagList = []
        #match the form like {type_name(tag_name:default_val)}
        tag_pattern = r"\{([0-9a-zA-Z_]+)\(([0-9a-zA-Z_]+)(?:|\:(?P<def>.+))\)(?:|(?P<view>!))\}"
        tag_compiler = re.compile(tag_pattern)
        for tag in self.caseData['data']['var'].split(','):
            result = tag_compiler.match(tag)
            tagList.append("{%s(%s:%s)}"%(result.group(1), result.group(2), result.group('def')))
        return tagList
        
    def setupLabel(self):
        tag_pattern = r'\{(?P<type>[0-9a-zA-Z_]+)\((?P<name>[0-9a-zA-Z_]+)\)\}'
        tag_compiler =re.compile(tag_pattern)
        tag_list = tag_compiler.findall(self.insertData['data']['value'])
        #setting layout
        settingWidget = OkTagSetting(tag_list)
        return settingWidget
        
    def saveCase(self):
        pass
        
    def paintEvent(self, event):
        self.setGeometry(QtCore.QRect(200, 0, self.parent().width() - 200 ,  self.parent().height()))
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(50,  50,  50))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.end()
        event.accept()
