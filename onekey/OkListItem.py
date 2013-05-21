from PyQt4 import QtGui, QtCore, Qt

class OkListItem(QtGui.QListWidgetItem):
    def __init__(self, text,  parent=None,  type=QtGui.QListWidgetItem.UserType):
        QtGui.QListWidgetItem.__init__(self, text,  parent, type)
        tmpBrush = QtGui.QBrush(QtGui.QColor(238,  238,  238))
        #tmpBrush = QtGui.QBrush()
        #tmpBrush.setTextureImage(QtGui.QImage(":/images/itembg_1x40.png"))
        self.setBackground(tmpBrush)
        self.setFlags(Qt.Qt.ItemIsUserCheckable|Qt.Qt.ItemIsEnabled|Qt.Qt.ItemIsDragEnabled)
        self.setWhatsThis("hello")
        self.setFont(QtGui.QFont("微软雅黑", 12))
        self.setTextColor(QtGui.QColor(59,  66,  76))
        self.setSizeHint(QtCore.QSize(200, 40))
        self.state = False
    
    def setItemSelected(self, item):
        if self.listWidget().selectedItem is not None:
            self.listWidget().selectedItem.state = False
            tmpBrush = QtGui.QBrush(QtGui.QColor(238,  238,  238))
            self.listWidget().selectedItem.setBackground(tmpBrush)
        self.state = True
        self.listWidget().selectedItem = item

class OkAddonWidget(QtGui.QWidget):
    """
    work as a cover on OkListItem
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.parent =parent
        vlayout = QtGui.QHBoxLayout()
        verticalSpacer = QtGui.QSpacerItem(20, 30, 7, 0)
        vlayout.setDirection(QtGui.QBoxLayout.RightToLeft)        
        vlayout.addWidget(OkPutinButton())
        vlayout.addSpacerItem(verticalSpacer)
        self.setLayout(vlayout)
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        if not self.parent.state:
            tmpBrush = QtGui.QBrush(QtGui.QColor(33,  133,  197))
            self.parent.setBackground(tmpBrush)
            event.accept()
        
    def leaveEvent(self, event):
        if not self.parent.state:
            tmpBrush = QtGui.QBrush(QtGui.QColor(238,  238,  238))
            self.parent.setBackground(tmpBrush)
            event.accept()
            
    def mousePressEvent(self, event):
        if event.buttons() == Qt.Qt.LeftButton:
            tmpBrush = QtGui.QBrush(QtGui.QColor(111,  111,  111))
            self.parent.setBackground(tmpBrush)
            self.parent.setItemSelected(self.parent)
            event.accept()
        
class OkPencilButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setMaximumSize(18, 18)
        self.setFlat(1)
        self.setStyleSheet("QPushButton{"
                    "height: 18px;"
                    "width: 18px;"
                    "background: url(:/images/pencil_18x18_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/pencil_18x18_blue.png)"
                "}")
        
    def mousePressEvent(self, event):
        #self.parent().parent().parent().itemPressed.connect(self.parent().parent().parent().pressItem)
        event.accept()

class OkPutinButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setMaximumSize(24, 24)
        self.setFlat(1)
        self.setStyleSheet("QPushButton{"
                    "height: 18px;"
                    "width: 18px;"
                    "background: url(:/images/putin_24x24_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/pencil_18x18_blue.png)"
                "}")
        
    def mousePressEvent(self, event):
        self.topLevelWidget().showArgSetPad(self.parent().parent)
        event.accept()
