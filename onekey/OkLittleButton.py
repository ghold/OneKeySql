from PyQt4 import QtGui, QtCore, Qt
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
        if not self.parent.isSelected():
            tmpBrush = QtGui.QBrush(QtGui.QColor(33,  133,  197))
            self.parent.setBackground(tmpBrush)
            event.accept()
        
    def leaveEvent(self, event):
        if not self.parent.isSelected():
            tmpBrush = QtGui.QBrush(QtGui.QColor(238,  238,  238))
            self.parent.setBackground(tmpBrush)
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
        #self.parent().parent().parent().itemPressed.connect(self.parent().parent().parent().pressItem)
        event.accept()
        
