from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkModuleButton import OkModuleButton
from OkToolBar import OkMainToolBar
from OkModel import OkModel
from OkXmlHandler import OkTestcaseHandler, OkTestunitHandler
from OkListItem import OkListItem
from OkEditWidget import OkEditWidget

class MainWindow(QtGui.QWidget):
    editWidget = None
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.CustomizeWindowHint|Qt.Qt.WindowSystemMenuHint)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(QtCore.QRect().adjusted(self.screen.width()/2 - 500, self.screen.height()/2 - 300, 
                self.screen.width()/2 + 500,  self.screen.height()/2 + 300))
                
        self.toolBar = OkMainToolBar(self)

        # Set up the model.
        self.model = OkModel("testcase/testcase.xml", OkTestcaseHandler)
        caseList = self.model.makeupTestList()
        caseList.itemClicked.connect(self.updateStepList)
        stepList = self.model.makeupStepList(caseList.item(0))
        
        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        verticalSpacer = QtGui.QSpacerItem(20, 30)
        tcLogo = QtGui.QImage(":/images/tc.png")
        tuLogo = QtGui.QImage(":/images/tu.png")
        self.tcButton = OkModuleButton("测试用例", tcLogo)
        self.tuButton = OkModuleButton("测试单元", tuLogo)

        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        self.mainSplitter = QtGui.QSplitter()
        self.mainSplitter.setHandleWidth(1)
        self.mainSplitter.setChildrenCollapsible(False)
        gridLayout.addWidget(self.mainSplitter,  1, 1)
        #gridLayout.addItem(verticalSpacer, 1, 2)
        
        moduleWidget = QtGui.QWidget()
        moduleLayout = QtGui.QVBoxLayout(moduleWidget)
        moduleLayout.addWidget(self.tcButton, 0, Qt.Qt.AlignTop)
        moduleLayout.addWidget(self.tuButton, 1, Qt.Qt.AlignTop)
        
        self.mainSplitter.addWidget(moduleWidget)
        self.mainSplitter.addWidget(caseList)
        self.mainSplitter.addWidget(stepList)
        self.mainSplitter.setStretchFactor(2, 1)
        self.setLayout(gridLayout)

        self.setWindowTitle("OneKeySql")
 
    @pyqtSlot(OkListItem)
    def updateStepList(self, item):
        stepList = self.model.makeupStepList(item)
        self.mainSplitter.widget(2).setParent(None)
        self.mainSplitter.addWidget(stepList)
        self.mainSplitter.setStretchFactor(2, 1)
        self.editWidget = OkEditWidget(self)
        self.editWidget.show()

    def mousePressEvent(self,event):
        
       if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.isMaximized():
            self.move(event.globalPos() - self.dragPosition)
            event.accept() 
    
        
    def paintEvent(self,  event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(Qt.Qt.white)
        tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()
        
    def exit(self):
        self.close()
