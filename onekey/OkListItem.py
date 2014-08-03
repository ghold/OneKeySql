from PyQt4 import QtCore, Qt
from PyQt4.QtCore import pyqtSlot

class OkListItem(Qt.QListWidgetItem):
    def __init__(self, text, parent=None,  type=Qt.QListWidgetItem.UserType):
        Qt.QListWidgetItem.__init__(self, text, parent, type)
        
        #set background
        image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
        image.fill(Qt.QColor(238,  238,  238))
        image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
        brush = Qt.QBrush()
        brush.setTextureImage(image)
        self.setBackground(brush)
        
        self.setFlags(Qt.Qt.ItemIsUserCheckable|Qt.Qt.ItemIsEnabled|Qt.Qt.ItemIsDragEnabled)
        self.setFont(Qt.QFont("微软雅黑", 12))
        self.setTextColor(Qt.QColor(110,  110,  110))
        self.setSizeHint(QtCore.QSize(200, 41))
        self.state = False
    
    def setItemSelected(self, item):
        if self.listWidget().selectedItem is not None:
            self.listWidget().selectedItem.state = False
            image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
            image.fill(Qt.QColor(238,  238,  238))
            image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
            brush = Qt.QBrush()
            brush.setTextureImage(image)
            self.listWidget().selectedItem.setBackground(brush)
            self.listWidget().selectedItem.setTextColor(Qt.QColor(110,  110,  110))
        self.state = True
        self.listWidget().selectedItem = item
        
class OkTreeItem(Qt.QTreeWidgetItem):
    def __init__(self, text, parent=None,  type=Qt.QTreeWidgetItem.Type):
        Qt.QTreeWidgetItem.__init__(self, parent, type)
        self.setText(0, text)
        
        #set background
        image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
        image.fill(Qt.QColor(238,  238,  238))
        image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
        brush = Qt.QBrush()
        brush.setTextureImage(image)
        self.setBackground(0, brush)
        
        self.setFlags(Qt.Qt.ItemIsUserCheckable|Qt.Qt.ItemIsEnabled|Qt.Qt.ItemIsDragEnabled)
        self.setFont(0, Qt.QFont("微软雅黑", 12))
        self.setTextColor(0, Qt.QColor(110,  110,  110))
        self.setSizeHint(0, QtCore.QSize(200, 41))
        
        self.state = False
        
    def setItemSelected(self, item):
        if self.treeWidget().selectedItem is not None:
            self.treeWidget().selectedItem.state = False
            image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
            image.fill(Qt.QColor(238,  238,  238))
            image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
            brush = Qt.QBrush()
            brush.setTextureImage(image)
            self.treeWidget().selectedItem.setBackground(0, brush)
            self.treeWidget().selectedItem.setTextColor(0, Qt.QColor(110,  110,  110))
        self.state = True
        self.treeWidget().selectedItem = item

class OkAddonWidget(Qt.QWidget):
    """
    work as a cover on OkTreeItem
    """
    def __init__(self, tooltip, item, parent=None):
        Qt.QWidget.__init__(self, parent)
        #self.toolTip = OkToolTip(tooltip)
        self.setToolTip(tooltip)
        self.item =item
        self.vlayout = Qt.QHBoxLayout()
        self.vlayout .setDirection(Qt.QBoxLayout.RightToLeft)
        
        self.setLayout(self.vlayout)
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        if not self.item.state:
            image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
            image.fill(Qt.QColor(77,  166,  234))
            image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
            brush = Qt.QBrush()
            brush.setTextureImage(image)
            self.item.setBackground(0, brush)
            self.item.setTextColor(0, Qt.QColor(255,  255,  255))
            
            #point = self.mapTo(self.topLevelWidget(), self.geometry().topLeft())
            #self.toolTip.setParent(self.topLevelWidget())
            #self.toolTip.setGeometry(point.x() - 10, (point.y() + 42 - 2*10)/2,
                    #self.geometry().width() + 20, self.geometry().height() + 20)
            #self.toolTip.show()
            event.accept()
        
    def leaveEvent(self, event):
        if not self.item.state:
            image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
            image.fill(Qt.QColor(238,  238,  238))
            image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
            brush = Qt.QBrush()
            brush.setTextureImage(image)
            self.item.setBackground(0, brush)
            self.item.setTextColor(0, Qt.QColor(110,  110,  110))
            event.accept()

class OkCaseAddon(OkAddonWidget):
    def __init__(self, tooltip, item, type, parent=None):
        OkAddonWidget.__init__(self, tooltip, item, parent)
        

class OkExecAddon(OkAddonWidget):
    def __init__(self, tooltip, item, type, parent=None):
        OkAddonWidget.__init__(self, tooltip, item, parent)
        verticalSpacer = Qt.QSpacerItem(20, 20, 7, 0)
        self.vlayout.addWidget(OkPutinButton())
        self.vlayout.addSpacerItem(verticalSpacer)
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.Qt.LeftButton and not self.item.state:
            #change background
            image = Qt.QImage(1, 41, Qt.QImage.Format_RGB32)
            image.fill(Qt.QColor(221, 221, 221))
            image.setPixel(0, 39, Qt.qRgba(33, 133, 197, 255))
            image.setPixel(0, 40, Qt.qRgba(255, 255, 255, 255))
            brush = Qt.QBrush()
            brush.setTextureImage(image)
            self.item.setBackground(0, brush)
            self.item.setTextColor(0, Qt.QColor(59,  66,  76))
            self.item.setItemSelected(self.item)
            #show info
            infoWidget = self.item.treeWidget().infoWidget
            infoWidget.infoGeneratorUTF8(self.item)
            event.accept()
    
class OkPencilButton(Qt.QPushButton):
    def __init__(self, parent=None):
        Qt.QPushButton.__init__(self, parent)
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
        self.state = False
        
    def mousePressEvent(self, event):
        caseList = self.parent().parent().parent()
        if caseList.editState:
            caseList.itemPressed.disconnect(caseList.pressItem)
            caseList.itemPressed.connect(self.topLevelWidget().updateStepList)
            self.topLevelWidget().mainSplitter.widget(2).setParent(None)
            self.topLevelWidget().mainSplitter.widget(1).setStretchFactor(1, 1)
            caseList.editState = False
            event.accept()
        else:
            caseList.itemPressed.disconnect(self.topLevelWidget().updateStepList)
            caseList.itemPressed.connect(caseList.pressItem)
            unitList = self.topLevelWidget().model.makeupUnitList()
            self.topLevelWidget().mainSplitter.addWidget(unitList)
            caseList.editState = True
            event.accept()

class OkPutinButton(Qt.QPushButton):
    def __init__(self, parent=None):
        Qt.QPushButton.__init__(self, parent)
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
        self.topLevelWidget().showArgSetPad(self.parent().item)
        event.accept()
##disable
class OkToolTip(Qt.QTextEdit):
    def __init__(self, text, parent=None):
        Qt.QTextEdit.__init__(self, text, parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #656565"
                "}")
        self.setSizePolicy(6, 6)
        
    def leaveEvent(self, event):
        self.hide()
        event.accept()
