from PyQt4 import QtGui, QtCore, Qt
from OkModuleButton import OkModuleButton
from OkToolBar import OkToolBar
from OkModel import OkModel
from OkListWidget import OkListWidget
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
        self.model = OkModel("testcase.xml", OkTestcaseHandler)
        print(self.model.invisibleRootItem().rowCount())
        
        #test
        listWidget = OkListWidget()
        listWidget.makeupCase("testcase.xml")
        #tmpGV
        
        

        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        verticalSpacer = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.nextButton = OkModuleButton("下一个")
        self.previousButton = OkModuleButton("上一个")

        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        mainSplitter = QtGui.QSplitter()
        mainSplitter.setHandleWidth(1)
        gridLayout.addWidget(mainSplitter,  1, 1, 1, 1)
        
        moduleWidget = QtGui.QWidget()
        moduleScene = QtGui.QVBoxLayout(moduleWidget)
        moduleScene.addWidget(self.nextButton, 0, Qt.Qt.AlignTop)
        moduleScene.addWidget(self.previousButton, 1, Qt.Qt.AlignTop)
        
        mainSplitter.addWidget(moduleWidget)
        
        mainSplitter.addWidget(listWidget)
        self.setLayout(gridLayout)

        self.setWindowTitle("Delegate Widget Mapper")
 
    def updateButtons(self, row):
        self.previousButton.setEnabled(row > 0)
        self.nextButton.setEnabled(row < self.model.rowCount() - 1)

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
