from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkModuleButton import OkModuleButton
from OkToolBar import OkMainToolBar
from OkModel import OkModel
from OkXmlHandler import OkTestcaseHandler, OkTestunitHandler
from OkInfoWidget import OkInfoWidget
from OkListItem import OkListItem
from OkEditPad import OkEditPad
from OkArgSetPad import OkArgSetPad

class MainWindow(QtGui.QWidget):
    editWidget = None
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.CustomizeWindowHint|Qt.Qt.WindowSystemMenuHint)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(QtCore.QRect().adjusted(self.screen.width()/2 - 500, self.screen.height()/2 - 300, 
                self.screen.width()/2 + 500,  self.screen.height()/2 + 300))
                
        self.toolBar = OkMainToolBar(self)
        self.setWindowTitle("OneKeySql")
        
        # Set up the model.
        self.model = OkModel("testcase/testcase.xml", OkTestcaseHandler)
        self.setupModel()
        
        # Set up the widgets.
        self.Spacer = QtGui.QSpacerItem(20, 30)
        tcLogo = QtGui.QImage(":/images/tc.png")
        tuLogo = QtGui.QImage(":/images/tu.png")
        txButton = OkModuleButton("测试执行", tcLogo)
        tcButton = OkModuleButton("测试用例", tcLogo)
        tuButton = OkModuleButton("测试单元", tuLogo)
        #buttonGroup
        self.moduleGroup = QtGui.QButtonGroup()
        self.moduleGroup.addButton(txButton, 1)
        self.moduleGroup.addButton(tcButton, 2)
        self.moduleGroup.addButton(tuButton, 3)
        self.moduleGroup.buttonClicked.connect(self.moduleChange)
        #mainSplitter
        self.mainSplitter = QtGui.QSplitter()
        self.mainSplitter.setHandleWidth(1)
        self.mainSplitter.setChildrenCollapsible(False)
        #moduleWidget
        moduleWidget = QtGui.QWidget()
        moduleLayout = QtGui.QVBoxLayout(moduleWidget)
        moduleLayout.addWidget(txButton, 0, Qt.Qt.AlignTop)
        moduleLayout.addWidget(tcButton, 0, Qt.Qt.AlignTop)
        moduleLayout.addWidget(tuButton, 1, Qt.Qt.AlignTop)
        self.mainSplitter.addWidget(moduleWidget)
        #mainLayout
        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(self.Spacer, 0, 0, 1, 4)
        gridLayout.addItem(self.Spacer, 1, 0)
        gridLayout.addWidget(self.mainSplitter,  1, 1)
        
        self.setLayout(gridLayout)
        
        #default
        self.mainSplitter.addWidget(self.caseExecModule())
        self.mainSplitter.setStretchFactor(1, 1)
        
    def setupModel(self):
        self.caseList = self.model.makeupTestList("CaseExec")
        self.caseList.itemClicked.connect(self.updateStepList)
        self.stepList = self.model.makeupStepList(self.caseList.item(0))
        
    def caseEditModule(self):
        #moduleSplitter
        moduleSplitter = QtGui.QSplitter()
        moduleSplitter.setHandleWidth(1)
        moduleSplitter.setChildrenCollapsible(False)
        #
        self.setupModel()
        moduleSplitter.addWidget(self.caseList)
        moduleSplitter.addWidget(self.stepList)
        moduleSplitter.setStretchFactor(1, 1)
        
        return moduleSplitter
        
    def caseExecModule(self):
        #moduleSplitter
        moduleSplitter = QtGui.QSplitter()
        moduleSplitter.setHandleWidth(1)
        moduleSplitter.setChildrenCollapsible(False)
        #
        self.setupModel()
        moduleSplitter.addWidget(self.caseList)
        okInfoWidget = OkInfoWidget()
        moduleSplitter.addWidget(okInfoWidget)
        moduleSplitter.setStretchFactor(1, 1)
        self.caseList.itemPressed.connect(okInfoWidget.infoGeneratorUTF8)
        return moduleSplitter
        
    @pyqtSlot(OkModuleButton)
    def moduleChange(self, button):
        if self.moduleGroup.id(button) == 1:
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.addWidget(self.caseExecModule())
            self.mainSplitter.setStretchFactor(1, 1)
        elif self.moduleGroup.id(button)  == 2:
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.addWidget(self.caseEditModule())
            self.mainSplitter.setStretchFactor(1, 1)
              
    @pyqtSlot(OkListItem)
    def updateStepList(self, item):
        stepList = self.model.makeupStepList(item)
        self.mainSplitter.widget(1).widget(1).setParent(None)
        self.mainSplitter.widget(1).addWidget(stepList)
        self.mainSplitter.widget(1).setStretchFactor(1, 1)
        self.editWidget = OkArgSetPad(item.data(Qt.Qt.UserRole), self)
        self.editWidget.show()

    def mousePressEvent(self,event):
        
       if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.isMaximized():
            #self.move(event.globalPos() - self.dragPosition)
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
