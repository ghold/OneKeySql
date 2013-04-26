from PyQt4 import QtGui, QtCore, Qt
from OkToolBar import OkEditToolBar
from OkLabel import OkEditWidgetLabel, OkTagLabel
from OkTextEdit import OkTextEdit
from OkTagWidget import OkTagWidget
from OkScrollBar import OkScrollBar

class OkEditWidget(QtGui.QWidget):
    editWidget = None
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.CustomizeWindowHint|Qt.Qt.WindowSystemMenuHint)
        
        #add toolBar
        self.toolBar = OkEditToolBar(self)
        
        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        horizontalSpacer1 = QtGui.QSpacerItem(10, 1000, 7, 7)
        verticalSpacer = QtGui.QSpacerItem(20, 30)
        tagLabel = OkEditWidgetLabel("标签")
        tagWidget = OkTagWidget()
        settingLabel = OkEditWidgetLabel("设置")
        settingLabel1 = OkTagLabel("设置")
        settingLabel2 = OkTagLabel("设置")
        settingLabel3 = OkTagLabel("设置")
        
        #add layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        editLayout = QtGui.QVBoxLayout()
        
        #setting layout
        settingLayout = QtGui.QFormLayout()
        settingLayout.addRow(settingLabel1, OkTextEdit())
        settingLayout.addRow(settingLabel2, OkTextEdit())
        settingLayout.addRow(settingLabel3, OkTextEdit())
        
        # add the widgets.
        editLayout.addWidget(tagLabel, 0, Qt.Qt.AlignTop)
        editLayout.addWidget(tagWidget, 1, Qt.Qt.AlignTop)
        editLayout.addWidget(settingLabel, 2, Qt.Qt.AlignTop)
        editLayout.addLayout(settingLayout, 0)
        editLayout.addSpacerItem(horizontalSpacer1)
        
        gridLayout.addLayout(editLayout, 1, 1)
        
        self.setLayout(gridLayout)
                
    def paintEvent(self, event):
        self.toolBar.update()
        self.setGeometry(QtCore.QRect(0, 0, self.parent().width()/2 ,  self.parent().height()))
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(62,  69,  76))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.end()
        event.accept()
