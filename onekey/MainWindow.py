from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot
from OkButton import *
from OkToolBar import OkMainToolBar
from OkModel import OkModel
from OkXmlHandler import OkTestcaseHandler, OkTestunitHandler
from OkInfoWidget import OkInfoWidget
from OkListItem import OkListItem
from OkListItem import OkTreeItem
from OkCaseEditPad import OkCaseEditPad
from OkArgSetPad import OkArgSetPad
from OkAddCase import OkAddCase
from OkXmlWriter import OkTestcaseWriter
from OkCover import OkCover
from OkSplitter import OkSplitter
from OkBasket import OkBasket
import os

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
        self.model = OkModel(( "testcase/testcase.xml", OkTestcaseHandler, 'case'),
                            ("testunit/testunit.xml", OkTestunitHandler, 'unit'),
                            ("testunit/spec.xml", OkTestunitHandler, 'unit'))
        
        # Set up the widgets.
        self.Spacer = QtGui.QSpacerItem(20, 30)
        txButton = OkModuleButton("测试执行", ":/images/tx_35x35.png")
        txButton.setChecked(True)
        tcButton = OkModuleButton("测试用例", ":/images/tc_35x35.png")
        #buttonGroup
        self.moduleGroup = QtGui.QButtonGroup()
        self.moduleGroup.addButton(txButton, 1)
        self.moduleGroup.addButton(tcButton, 2)
        self.moduleGroup.buttonClicked.connect(self.moduleChange)
        #basket
        self.basket = OkBasket()
        self.basket.hide()
        #mainSplitter
        self.mainSplitter =OkSplitter()
        #moduleWidget
        moduleWidget = QtGui.QWidget()
        moduleLayout = QtGui.QVBoxLayout(moduleWidget)
        moduleLayout.addWidget(txButton, 0, Qt.Qt.AlignTop)
        moduleLayout.addWidget(tcButton, 1, Qt.Qt.AlignTop)
        moduleLayout.addWidget(self.basket, 1, Qt.Qt.AlignBottom)
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
        
    def caseEditModule(self):
        #moduleSplitter
        moduleSplitter = OkSplitter()
        
        #setup case list
        self.caseList = self.model.makeupCaseList()
        self.caseList.itemPressed.connect(self.updateStepList)
        self.caseList.itemDoubleClicked.connect(self.openEditMode)
#        stepList = self.model.makeupStepList(self.caseList.item(0))
        
        #completer
        wordList = ["中转" ,  "运输" ,  "散货" ,  "收仓"]
        completer = QtGui.QCompleter(wordList)
        
        #
        searchEdit = QtGui.QLineEdit()
        searchEdit.setCompleter(completer)
        searchEdit.textChanged.connect(self.caseList.search)
        
        self.addButton = OkAddCaseButton()
        self.addButton.pressed.connect(self.pushAddCase)
        self.cancelButton = OkCancelButton()
        self.cancelButton.pressed.connect(self.pushCancel)
        
        searchLayout = QtGui.QHBoxLayout()
        searchLayout.addWidget(searchEdit)
        searchLayout.addWidget(self.addButton)
        searchLayout.addWidget(self.cancelButton)
        self.cancelButton.hide()
        
        #
        self.addingWidget = OkAddCase()
        self.addingWidget.hide()
        #
        topLayout = QtGui.QVBoxLayout()
        topLayout.addLayout(searchLayout)
        topLayout.addWidget(self.addingWidget)
        
        #
        caseLayout = QtGui.QVBoxLayout()
        caseLayout.addLayout(topLayout)
        caseLayout.addWidget(self.caseList)
        
        caseWidget = QtGui.QWidget()
        caseWidget.setLayout(caseLayout)
        moduleSplitter.addWidget(caseWidget)
#        moduleSplitter.addWidget(stepList)
#        moduleSplitter.setStretchFactor(1, 1)

        return moduleSplitter
        
    def caseExecModule(self):
        #moduleSplitter
        moduleSplitter = OkSplitter()
        #setup exec list
        self.caseList = self.model.makeupExecList()
        #completer
        wordList = ["中转" ,  "运输" ,  "散货" ,  "收仓"]
        completer = QtGui.QCompleter(wordList)
        #caseWidget
        caseWidget = QtGui.QWidget()
        lineEdit = QtGui.QLineEdit()
        lineEdit.setCompleter(completer)
        lineEdit.textChanged.connect(self.caseList.search)
        caseLayout = QtGui.QVBoxLayout()
        caseLayout.addWidget(lineEdit)
        caseLayout.addWidget(self.caseList)
        caseWidget.setLayout(caseLayout)
        moduleSplitter.addWidget(caseWidget)
        #infoWidget
        okInfoWidget = OkInfoWidget()
        self.caseList.setOkInfo(okInfoWidget)
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
    
#    @pyqtSlot(OkListItem)
#    def updateStepList(self, item):
#        self.stepList = self.model.makeupStepList(item)
#        self.stepList.itemPressed.connect(self.stepList.pressItem)
#        if self.mainSplitter.widget(1).widget(1) is not None:
#            self.mainSplitter.widget(1).widget(1).setParent(None)
#        self.mainSplitter.widget(1).addWidget(self.stepList)
#        self.mainSplitter.widget(1).setStretchFactor(1, 1)

    @pyqtSlot(OkTreeItem)
    def updateStepList(self, item):
        if item.childCount() == 0:
            self.stepList = self.model.makeupStepList(item)
            self.stepList.itemPressed.connect(self.stepList.pressItem)
            if self.mainSplitter.widget(1).widget(1) is not None:
                self.mainSplitter.widget(1).widget(1).setParent(None)
            self.mainSplitter.widget(1).addWidget(self.stepList)
            self.mainSplitter.widget(1).setStretchFactor(1, 1)
    
    @pyqtSlot(OkTreeItem)
    def openEditMode(self, item):
        if item.childCount() == 0:
            if item.treeWidget().editState and item == item.treeWidget().selectedItem:
                item.treeWidget().itemPressed.connect(self.updateStepList)
                item.treeWidget().itemPressed.disconnect(item.treeWidget().pressItem)
                self.mainSplitter.widget(2).setParent(None)
                self.mainSplitter.widget(1).setStretchFactor(1, 1)
                for btn in self.moduleGroup.buttons():
                    btn.setEnabled(True)
                self.addButton.setEnabled(True)
                item.treeWidget().editState = False
                #change background
                image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
                image.fill(QtGui.QColor(238,  238,  238))
                image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
                brush = QtGui.QBrush()
                brush.setTextureImage(image)
                item.setBackground(0, brush)
                item.setTextColor(0, QtGui.QColor(110,  110,  110))
                item.state = False
                item.treeWidget().selectedItem = None
                
            elif not item.treeWidget().editState:
                self.updateStepList(item)
                item.treeWidget().itemPressed.disconnect(self.updateStepList)
                item.treeWidget().itemPressed.connect(item.treeWidget().pressItem)
                #setup unitList
                unitList = self.model.makeupUnitList()
                unitList.itemPressed.connect(unitList.pressItem)
                #completer
                wordList = ["中转" ,  "运输" ,  "散货" ,  "收仓"]
                completer = QtGui.QCompleter(wordList)
                #unitWidget
                unitWidget = QtGui.QWidget()
                lineEdit = QtGui.QLineEdit()
                lineEdit.setCompleter(completer)
                lineEdit.textChanged.connect(unitList.search)
                unitLayout = QtGui.QVBoxLayout()
                unitLayout.addWidget(lineEdit)
                unitLayout.addWidget(unitList)
                unitWidget.setLayout(unitLayout)
                
                self.mainSplitter.addWidget(unitWidget)
                for btn in self.moduleGroup.buttons():
                    btn.setEnabled(False)
                self.addButton.setEnabled(False)
                item.treeWidget().editState = True
                #change background
                image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
                image.fill(QtGui.QColor(221, 221, 221))
                image.setPixel(0, 39, QtGui.qRgba(33, 133, 197, 255))
                image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
                brush = QtGui.QBrush()
                brush.setTextureImage(image)
                item.setBackground(0, brush)
                item.setTextColor(0, QtGui.QColor(59,  66,  76))
                item.setItemSelected(item)
            
    def showArgSetPad(self, item):
        self.cover = OkCover(self)
        self.editWidget = OkArgSetPad(item.data(0, Qt.Qt.UserRole), self)
        self.cover.show()
        self.editWidget.show()
        
    def showCaseEditPad(self, item, data):
        self.cover = OkCover(self)
        self.editWidget = OkCaseEditPad(item, data, self)
        self.cover.show()
        self.editWidget.show()
        
    @pyqtSlot()    
    def pushAddCase(self):
        if self.addingWidget.isHidden():
            self.cancelButton.show()
            self.addingWidget.show()
        else:
            name, cate, desc = self.addingWidget.getNameAndDesc()
            if len(name.strip()) >0 and len(cate.strip()) > 0:
                path =  os.environ['ONEKEY_HOME']
                writer = OkTestcaseWriter(path  + '/testcase/testcase.xml')
                writer.createCase(name, cate, desc)
                self.cancelButton.hide()
                self.addingWidget.hide()
                self.model.update()
                self.moduleChange(self.moduleGroup.button(2))
            else:
                self.addingWidget.nameEdit.setFocus()
    
    @pyqtSlot()
    def pushCancel(self):
        self.cancelButton.hide()
        self.cancelButton.setDown(False)
        self.addingWidget.hide()

    def mousePressEvent(self,event):
       if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.isMaximized():
            #self.move(event.globalPos() - self.dragPosition)
            event.accept()
            
    def updateCaseList(self):
        self.model.update()
        self.moduleChange(self.moduleGroup.button(2))
        
    def exit(self):
        self.close()
