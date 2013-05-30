from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkButton import OkModuleButton
from OkToolBar import OkMainToolBar
from OkModel import OkModel
from OkXmlHandler import OkTestcaseHandler, OkTestunitHandler
from OkInfoWidget import OkInfoWidget
from OkListItem import OkListItem
from OkCaseEditPad import OkCaseEditPad
from OkArgSetPad import OkArgSetPad

class MainWindow(QtGui.QFrame):
    editWidget = None
    def __init__(self,  parent=None):
        QtGui.QFrame.__init__(self,  parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.WindowSystemMenuHint|Qt.Qt.WindowMinMaxButtonsHint)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(QtCore.QRect().adjusted(self.screen.width()/2 - 500, self.screen.height()/2 - 300, 
                self.screen.width()/2 + 500,  self.screen.height()/2 + 300))
        self.setObjectName("MainWindow")
        self.setStyleSheet("QFrame#MainWindow{"
                    "background-color: #FFF;"
                    "border: 1px solid #ddd;"
                "}")
        self.toolBar = OkMainToolBar(self)
        self.setWindowTitle("OneKeySql")
        
        # Set up the model.
        self.model = OkModel(("testcase/testcase.xml", OkTestcaseHandler, 'case'), ("testunit/testunit.xml", OkTestunitHandler, 'unit'))
        
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
        pass
        #self.caseList.itemClicked.connect(self.updateStepList)
        #self.stepList = self.model.makeupStepList(self.caseList.item(0))
        
    def caseEditModule(self):
        #moduleSplitter
        moduleSplitter = QtGui.QSplitter()
        moduleSplitter.setHandleWidth(1)
        moduleSplitter.setChildrenCollapsible(False)
        
        #setup case list
        caseList = self.model.makeupCaseList()
        caseList.itemPressed.connect(self.updateStepList)
        caseList.itemDoubleClicked.connect(self.openEditMode)
        stepList = self.model.makeupStepList(caseList.item(0))
        
        caseWidget = QtGui.QWidget()
        lineEdit = QtGui.QLineEdit()
        caseLayout = QtGui.QVBoxLayout()
        caseLayout.addWidget(lineEdit)
        caseLayout.addWidget(caseList)
        caseWidget.setLayout(caseLayout)
        moduleSplitter.addWidget(caseWidget)
        moduleSplitter.addWidget(stepList)
        moduleSplitter.setStretchFactor(1, 1)

        return moduleSplitter
        
    def caseExecModule(self):
        #moduleSplitter
        moduleSplitter = QtGui.QSplitter()
        moduleSplitter.setHandleWidth(1)
        moduleSplitter.setChildrenCollapsible(False)
        #setup exec list
        caseList = self.model.makeupExecList()
        #completer
        wordList = ["中转" ,  "运输" ,  "散货" ,  "收仓"]
        completer = QtGui.QCompleter(wordList)
        #caseWidget
        caseWidget = QtGui.QWidget()
        lineEdit = QtGui.QLineEdit()
        lineEdit.setCompleter(completer)
        lineEdit.textChanged.connect(caseList.search)
        caseLayout = QtGui.QVBoxLayout()
        caseLayout.addWidget(lineEdit)
        caseLayout.addWidget(caseList)
        caseWidget.setLayout(caseLayout)
        moduleSplitter.addWidget(caseWidget)
        #infoWidget
        okInfoWidget = OkInfoWidget()
        caseList.setOkInfo(okInfoWidget)
        moduleSplitter.addWidget(okInfoWidget)
        moduleSplitter.setStretchFactor(1, 1)
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
    
    @pyqtSlot(OkListItem)
    def openEditMode(self, item):
        if item.listWidget().editState and item == item.listWidget().selectedItem:
            item.listWidget().itemPressed.connect(self.updateStepList)
            item.listWidget().itemPressed.disconnect(item.listWidget().pressItem)
            self.mainSplitter.widget(2).setParent(None)
            self.mainSplitter.widget(1).setStretchFactor(1, 1)
            item.listWidget().editState = False
            #change background
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(238,  238,  238))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            item.setBackground(brush)
            item.setTextColor(QtGui.QColor(110,  110,  110))
            item.state = False
            item.listWidget().selectedItem = None
            
        elif not item.listWidget().editState:
            self.updateStepList(item)
            item.listWidget().itemPressed.disconnect(self.updateStepList)
            item.listWidget().itemPressed.connect(item.listWidget().pressItem)
            unitList = self.model.makeupUnitList()
            unitList.itemPressed.connect(unitList.pressItem)
            self.mainSplitter.addWidget(unitList)
            item.listWidget().editState = True
            #change background
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(221, 221, 221))
            image.setPixel(0, 39, QtGui.qRgba(33, 133, 197, 255))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            item.setBackground(brush)
            item.setTextColor(QtGui.QColor(59,  66,  76))
            item.setItemSelected(item)
            
    def showArgSetPad(self, item):
        self.editWidget = OkArgSetPad(item.data(Qt.Qt.UserRole), self)
        self.editWidget.show()
        
    def showCaseEditPad(self, item, data):
        self.editWidget = OkCaseEditPad(item.data(Qt.Qt.UserRole), data, self)
        self.editWidget.show()

    def mousePressEvent(self,event):
       if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.isMaximized():
            #self.move(event.globalPos() - self.dragPosition)
            event.accept() 
        
    def exit(self):
        self.close()
