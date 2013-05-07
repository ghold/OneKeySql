from PyQt4 import QtGui, QtCore, Qt
from OkToolBar import OkEditToolBar
from OkLabel import OkEditWidgetLabel, OkTagLabel
from OkEdit import OkTextEdit, OkDateTimeEdit
import re

class OkArgSetPad(QtGui.QWidget):
    editWidget = None
    data = {}
    def __init__(self, data, parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.data = data
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        
        #add toolBar
        self.toolBar = OkEditToolBar(self)
        
        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        horizontalSpacer1 = QtGui.QSpacerItem(10, 1000, 7, 7)
        verticalSpacer = QtGui.QSpacerItem(20, 30)
        caseLabel = OkEditWidgetLabel("标签")
        
        #add layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        editLayout = QtGui.QVBoxLayout()
        
        settingWidget = self.setupLabel()
        
        # add the widgets.
        editLayout.addWidget(caseLabel, 0, Qt.Qt.AlignTop)
        editLayout.addWidget(settingWidget, 1, Qt.Qt.AlignTop)
        editLayout.addSpacerItem(horizontalSpacer1)
        
        gridLayout.addLayout(editLayout, 1, 1)
        
        self.setLayout(gridLayout)
        
    def setupLabel(self):
        #setting layout
        settingWidget = QtGui.QWidget()
        settingLayout = QtGui.QFormLayout()
        settingLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        settingLayout.setLabelAlignment(Qt.Qt.AlignRight)
        
        tag_pattern = r'\{(.+)\((.+)\)\}'
        tag_compiler = re.compile(tag_pattern)
        for tag in self.data['data']['var'].split(','):
            result = tag_compiler.match(tag)
            settingLayout.addRow(OkTagLabel(result.group(2)), OkTextEdit())
        
        settingWidget.setLayout(settingLayout)
        return settingWidget
        
    def paintEvent(self, event):
        self.setGeometry(QtCore.QRect(self.parent().width()/2, 0, self.parent().width()/2 ,  self.parent().height()))
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(50,  50,  50))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.end()
        event.accept()

