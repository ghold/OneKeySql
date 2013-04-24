from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkModuleButton import OkModuleButton
from OkToolBar import OkToolBar
from OkModel import OkModel
from OkXmlHandler import OkTestcaseHandler, OkTestunitHandler
from OkListItem import OkListItem

class MainWindow(QtGui.QWidget):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.CustomizeWindowHint|Qt.Qt.WindowSystemMenuHint)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(QtCore.QRect().adjusted(self.screen.width()/2 - 500, self.screen.height()/2 - 300, 
                self.screen.width()/2 + 500,  self.screen.height()/2 + 300))
                
        self.toolBar = OkToolBar(self)

        # Set up the model.
        self.model = OkModel("testcase/testcase.xml", OkTestcaseHandler)
        caseList = self.model.makeupTestList()
        caseList.itemClicked.connect(self.updateStepList)
        stepList = self.model.makeupStepList(caseList.item(0))
        stepList.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        
        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        verticalSpacer = QtGui.QSpacerItem(20, 30)
        self.nextButton = OkModuleButton("下一个")
        self.previousButton = OkModuleButton("上一个")

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
        moduleLayout.addWidget(self.nextButton, 0, Qt.Qt.AlignTop)
        moduleLayout.addWidget(self.previousButton, 1, Qt.Qt.AlignTop)
        
        self.mainSplitter.addWidget(moduleWidget)
        self.mainSplitter.addWidget(caseList)
        self.mainSplitter.addWidget(stepList)
        self.mainSplitter.setStretchFactor(2, 1)
        self.setLayout(gridLayout)

        self.setWindowTitle("Delegate Widget Mapper")
 
    @pyqtSlot(OkListItem)
    def updateStepList(self, item):
        stepList = self.model.makeupStepList(item)
        self.mainSplitter.widget(2).setParent(None)
        self.mainSplitter.addWidget(stepList)

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
