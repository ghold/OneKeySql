from PyQt4 import QtGui
from ui_previewer import Ui_Form
from xml.sax import parse
from TestunitHandler import TestunitHandler

class MainWindow(QtGui.QWidget,  Ui_Form):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self,  parent)
        #self.setWindowFlags(Qt.Qt.FramelessWindowHint)

        # Set up the model.
        self.setupModel()

        # Set up the widgets.
        nameLabel = QtGui.QLabel("Na&me:")
        nameEdit = QtGui.QLineEdit()
        addressLabel = QtGui.QLabel("&Address:")
        addressEdit = QtGui.QTextEdit()
        typeLabel = QtGui.QLabel("&Type:")
        typeComboBox = QtGui.QComboBox()
        self.nextButton = QtGui.QPushButton("&Next")
        self.previousButton = QtGui.QPushButton("&Previous")
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

        layout = QtGui.QGridLayout()
        layout.addWidget(nameLabel, 0, 0, 1, 1)
        layout.addWidget(nameEdit, 0, 1, 1, 1)
        layout.addWidget(self.previousButton, 0, 2, 1, 1)
        layout.addWidget(addressLabel, 1, 0, 1, 1)
        layout.addWidget(addressEdit, 1, 1, 2, 1)
        layout.addWidget(self.nextButton, 1, 2, 1, 1)
        layout.addWidget(typeLabel, 3, 0, 1, 1)
        layout.addWidget(typeComboBox, 3, 1, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle("Delegate Widget Mapper")
        self.mapper.toFirst()
 
    def setupModel(self):
        items = ("Home", "Work", "Other")
        self.typeModel = QtGui.QStringListModel(items, self)

        self.model = QtGui.QStandardItemModel(5, 3, self)
        
        test = TestunitHandler()
        parse("sample.xml",  test)
        
        names = ("Alice", "Bob", "Carol", "Donald", "Emma")
        addresses = test.testunits['data']['testunit_00002']['id']
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

            
    
        
    def exit(self):
        self.close()
