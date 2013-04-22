from PyQt4 import QtGui, QtCore, Qt
from ModuleButton import ModuleButton
from OkToolBar import OkToolBar
from xml.sax import parse
from OkXmlHandler import OkTestunitHandler
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
        self.setupModel()
        
        #test
        item1 = OkListItem("Hello")
        item2 = OkListItem("Hello")
        listWidget = QtGui.QListWidget()
        listWidget.setFrameStyle(QtGui.QFrame.NoFrame)
        listWidget.setSelectionMode(0)
        listWidget.setFocusPolicy(Qt.Qt.NoFocus)
        listWidget.addItem(item1)
        listWidget.addItem(item2)
        
        #tmpGV
        
        

        # Set up the widgets.
        horizontalSpacer = QtGui.QSpacerItem(20, 30)
        verticalSpacer = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        nameLabel = QtGui.QLabel("&Name:")
        nameEdit = QtGui.QLineEdit()
        addressLabel = QtGui.QLabel("&Address:")
        addressEdit = QtGui.QTextEdit()
        typeLabel = QtGui.QLabel("&Type:")
        typeComboBox = QtGui.QComboBox()
        self.nextButton = ModuleButton("下一个")
        self.previousButton = ModuleButton("上一个")
        nameLabel.setBuddy(nameEdit)
        addressLabel.setBuddy(addressEdit)
        typeLabel.setBuddy(typeComboBox)
        typeComboBox.setModel(self.typeModel)

        # Set up the mapper.
        self.mapper = QtGui.QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(nameEdit, 0)
        self.mapper.addMapping(addressEdit, 1)
        self.mapper.addMapping(typeComboBox, 2, 'currentIndex')

        # Set up connections and layouts.
        self.previousButton.clicked.connect(self.mapper.toPrevious)
        self.nextButton.clicked.connect(self.mapper.toNext)
        self.mapper.currentIndexChanged.connect(self.updateButtons)

        gridLayout = QtGui.QGridLayout()
        gridLayout.setOriginCorner(Qt.Qt.TopLeftCorner)
        gridLayout.addItem(horizontalSpacer, 0, 0, 1, 4)
        gridLayout.addItem(verticalSpacer, 1, 0)
        mainSplitter = QtGui.QSplitter()
        mainSplitter.setHandleWidth(1)
        gridLayout.addWidget(mainSplitter,  1, 1, 1, 1)
        
        moduleWidget = QtGui.QWidget()
        moduleScene = QtGui.QVBoxLayout(moduleWidget)
        moduleScene.addWidget(self.previousButton, 0, Qt.Qt.AlignTop)
        moduleScene.addWidget(self.nextButton, 1, Qt.Qt.AlignTop)
        
        mainSplitter.addWidget(moduleWidget)
        
        moduleWidget2 = QtGui.QWidget()
        moduleScene2 = QtGui.QVBoxLayout(moduleWidget2)
        moduleScene2.addWidget(nameLabel)
        moduleScene2.addWidget(addressLabel)
        
        mainSplitter.addWidget(listWidget)
        #layout.addWidget(nameLabel, 1, 2, 1, 1)
        #layout.addWidget(nameEdit, 1, 1, 1, 1)
        #layout.addWidget(self.previousButton, 1, 0, 1, 1)
        #layout.addWidget(addressLabel, 2, 2, 1, 1)
        #layout.addWidget(addressEdit, 2, 1, 2, 1)
        #layout.addWidget(self.nextButton, 2, 0, 1, 1)
        #layout.addWidget(typeLabel, 4, 0, 1, 1)
        #layout.addWidget(typeComboBox, 4, 1, 1, 1)
        self.setLayout(gridLayout)

        self.setWindowTitle("Delegate Widget Mapper")
        self.mapper.toFirst()
 
    def setupModel(self):
        items = ("Home", "Work", "Other")
        self.typeModel = QtGui.QStringListModel(items, self)

        self.model = QtGui.QStandardItemModel(5, 3, self)
        
        test = OkTestunitHandler()
        parse("sample.xml",  test)
        
        names = ("Alice", "Bob", "Carol", "Donald", "Emma")
        addresses = test.testunits['testunit_00002']['id']
        print(addresses)
        types = ("0", "1", "2", "0", "2")
        
        for row, name in enumerate(names):
            item = QtGui.QStandardItem(name)
            self.model.setItem(row, 0, item)
            item = QtGui.QStandardItem(addresses)
            self.model.setItem(row, 1, item)
            item = QtGui.QStandardItem(types[row])
            self.model.setItem(row, 2, item)
 
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
