from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkTagHandler import OkTagHandler
from OkToolBar import OkEditToolBar
from OkScroll import OkScrollArea
from OkButton import OkExecButton
from OkLabel import OkEditWidgetLabel, OkTagLabel
from OkPreviewWidget import OkPreviewWidget
from oracle.OkSqlHandler import OkSqlHandler
from OkRuntime import OkExecProcess
from OkConfig import OkConfig
from OkEdit import *
import re
import time

class OkArgSetPad(QtGui.QWidget):
    editWidget = None
    data = {}
    def __init__(self, data, parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.data = data
        self.config = OkConfig()
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(200, 0, self.parent().width() - 200 ,  self.parent().height()))
        
        #add toolBar
        self.toolBar = OkEditToolBar(self)
        
        # Set up the widgets.
        spacer = QtGui.QSpacerItem(20, 30)
        caseLabel = OkEditWidgetLabel("标签")
        previewLabel = OkEditWidgetLabel("预览")
        #comfireButton
        self.comfirmButton = OkExecButton("执行")
        self.comfirmButton.clicked.connect(self.sqlExec)
        
        #
        horizonLayout = QtGui.QHBoxLayout()
        horizonLayout.addWidget(previewLabel)
        horizonLayout.addWidget(self.comfirmButton )
        
        #add layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(spacer, 0, 0, 1, 4)
        gridLayout.addItem(spacer, 1, 0)
        editLayout = QtGui.QVBoxLayout()
        
        #previewWidget
        self.previewWidget = self.setupPreview()
        settingWidget = self.setupLabel()

        # add the widgets.
        if settingWidget is not None:
            editLayout.addWidget(caseLabel, 0, Qt.Qt.AlignTop)
            editLayout.addWidget(settingWidget, 0, Qt.Qt.AlignTop)
        editLayout.addLayout(horizonLayout, 0)
        editLayout.addWidget(self.previewWidget, 1)
        
        gridLayout.addLayout(editLayout, 1, 1)
        self.setLayout(gridLayout)
        
    def setupLabel(self):
        if len(self.data['data']['var']) == 0:
            return None
        #setting layout
        settingWidget = OkScrollArea()
        #label layout
        labelWidget = QtGui.QWidget()
        labelWidget.setStyleSheet("background-color: #323232;")
        labelLayout = QtGui.QFormLayout()
        labelLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        labelLayout.setLabelAlignment(Qt.Qt.AlignRight)
        
        #match the form like {type_name(tag_name:default_val)}
        tag_pattern = r"\{([0-9a-zA-Z_]+)\(([0-9a-zA-Z_]+)(?:|\:(?P<def>.+))\)(?:|(?P<view>!))\}"
        tag_compiler = re.compile(tag_pattern)
        for tag in self.data['data']['var'].split(','):
            result = tag_compiler.match(tag)
            tmp_default_value = result.group("def")
            default_value = ''
            #Globalconfig or user default 
            
            OkTagWidget = OkTagHandler.callback(result.group(1), result.group(2), tmp_default_value, None)
            OkTagWidget.ValueChanged.connect(self.previewWidget.tagValue)
            
            if tmp_default_value is not None and tmp_default_value[0] == "'":
                default_value = tmp_default_value.strip("'")
            else:
                default_value = self.config.callback(result.group("def"))
            
            if default_value is not None:
                OkTagWidget.setValue(default_value)
            if result.group("view") is  None:
                labelLayout.addRow(OkTagLabel(result.group(2)), OkTagWidget)
        if labelLayout.count() > 0:
            labelWidget.setLayout(labelLayout)
            settingWidget.setWidget(labelWidget)
            return settingWidget
        return None
    
    def setupPreview(self):
        previewWidget = OkPreviewWidget()
        previewWidget.setupData(self.data['data']['steps'])
        return previewWidget
    
    @pyqtSlot()
    def sqlExec(self):
        if len(self.previewWidget.toPlainText())  == 0:
            self.close()
            return
        
        thread = OkExecProcess(self.previewWidget.toPlainText())
        thread.start()
#        self.comfirmButton.setDisabled(True)
#        step_pattern = r";\n/\*Step [0-9 ]+.+\*/\n"
#        step_compiler = re.compile(step_pattern)
#        step_list = step_compiler.split(self.previewWidget.toPlainText())
#        sql_pattern = r";\n|/\*Step [0-9 ]+.+\*/\n|\n"
#        sql_compiler = re.compile(sql_pattern)
#        for val in step_list:
#            val = sql_compiler.sub(r' ', val)
#            #Don't need to add " at start or at end
#            if 'INSERT' in val:
#                OkSqlHandler.insertAction(val.strip())
#            else:
#                exec(val.strip())
        self.previewWidget.config.save()
        self.parent().cover.close()
        self.close()
        
        
    def paintEvent(self, event):
        self.setGeometry(QtCore.QRect(200, 0, self.parent().width() - 200 ,  self.parent().height()))
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(50,  50,  50))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.end()
        event.accept()

