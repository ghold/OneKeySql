from PyQt4 import Qt, QtCore, Qt
from OkToolBar import OkEditToolBar
from OkLabel import OkEditWidgetLabel
from OkButton import OkExecButton
from OkTagSetting import OkTagSetting
from OkTagBox import OkTagBox
from OkXmlWriter import OkTestcaseWriter
from PyQt4.QtCore import pyqtSlot
import re
import os

class OkCaseEditPad(Qt.QWidget):
    editWidget = None
    caseData = {}
    insertData = {}
    path =  os.environ['ONEKEY4499_HOME']
    def __init__(self, item, insertdata, parent=None):
        Qt.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(200, 0, self.parent().width() - 200 ,  self.parent().height()))
        self.item = item
        self.caseData = self.item.data(0, Qt.Qt.UserRole)
        self.insertData = insertdata
        #add toolBar
        self.toolBar = OkEditToolBar(self)
        
        # Set up the widgets.
        horizontalSpacer = Qt.QSpacerItem(20, 30)
        verticalSpacer = Qt.QSpacerItem(20, 30)
        #tag
        tagLabel = OkEditWidgetLabel("标签")
        self.labelTags = self.setupTag()
        self.tagWidget = OkTagBox(self.labelTags, self)
        settingLabel = OkEditWidgetLabel("设置")
        
        #add layout
        gridLayout = Qt.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        editLayout = Qt.QVBoxLayout()
        
        #setting layout
        self.settingWidget = self.setupTable()
        #comfireButton
        self.comfirmButton = OkExecButton("保存")
        self.comfirmButton.clicked.connect(self.saveCase)
        #
        horizonLayout = Qt.QHBoxLayout()
        horizonLayout.addWidget(settingLabel)
        horizonLayout.addWidget(self.comfirmButton )
        
        # add the widgets.
        editLayout.addWidget(tagLabel, 0, Qt.Qt.AlignTop)
        editLayout.addWidget(self.tagWidget, 0, Qt.Qt.AlignTop)
        editLayout.addLayout(horizonLayout, 0)
        if self.settingWidget is not None:
            editLayout.addWidget(self.settingWidget, 1)
        
        gridLayout.addLayout(editLayout, 1, 1)
        
        self.setLayout(gridLayout)
        
    def setupTag(self):
        tagList = []
        if len(self.caseData['data']['var']) == 0:
            return tagList
        #match the form like {type_name(tag_name:default_val)}
        tag_pattern = r"\{([0-9a-zA-Z_]+)\(([0-9a-zA-Z_]+)(?:|\:(?P<def>.+))\)(?:|(?P<view>!))\}"
        tag_compiler = re.compile(tag_pattern)
        for tag in self.caseData['data']['var'].split(','):
            result = tag_compiler.match(tag)
            tagList.append([result.group(1), result.group(2), result.group('def'),  result.group('view')])
        return tagList
    
    def setupTable(self):
        tag_pattern = r'\{(?P<type>[0-9a-zA-Z_]+)\((?P<name>[0-9a-zA-Z_]+)\)\}'
        tag_compiler =re.compile(tag_pattern)
        tag_list = tag_compiler.findall(self.insertData['data']['value'])
        #setting layout
        settingWidget = OkTagSetting(tag_list, self.labelTags, self.insertData)
        return settingWidget
        
    @pyqtSlot()
    def saveCase(self):
        data = self.settingWidget.setupModelDict()
        if data is None:
            return
        writer = OkTestcaseWriter(self.path + '/testcase/testcase.xml')
        writer.makeupElement(data, self.caseData['id'])
        self.parent().model.update()
        self.parent().model.updateCaseItem(self.item)
        self.parent().updateStepList(self.item)
        self.parent().cover.hide()
        self.close()
        
    def paintEvent(self, event):
        self.setGeometry(QtCore.QRect(200, 0, self.parent().width() - 200 ,  self.parent().height()))
        tmpPainter = Qt.QPainter()
        tmpPainter.begin(self)
        tmpBrush = Qt.QBrush(Qt.QColor(50,  50,  50))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.end()
        event.accept()

