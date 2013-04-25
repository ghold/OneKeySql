from PyQt4 import QtGui, QtCore, Qt
from OkToolBar import OkEditToolBar
from OkLabel import OkEditWidgetLabel
from OkTagWidget import OkTagWidget

class OkEditWidget(QtGui.QWidget):
    editWidget = None
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.CustomizeWindowHint|Qt.Qt.WindowSystemMenuHint)
        #add toolBar
        self.toolBar = OkEditToolBar(self)
        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        verticalSpacer = QtGui.QSpacerItem(20, 30)
        tagLabel = OkEditWidgetLabel("标签")
        tagWidget = OkTagWidget()
        contentLabel = OkEditWidgetLabel("内容")
        #add layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        
        editLayout = QtGui.QVBoxLayout()
        # Set up the widgets.
        editLayout.addWidget(tagLabel, 0, Qt.Qt.AlignTop)
        editLayout.addWidget(tagWidget, 1, Qt.Qt.AlignTop)
        editLayout.addWidget(contentLabel, 2, Qt.Qt.AlignTop)
        
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
