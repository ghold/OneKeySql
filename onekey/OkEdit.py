from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import pyqtSignal, pyqtSlot

class OkTextEdit(QtGui.QLineEdit):
    ValueChanged = pyqtSignal(str, str, str)
    def __init__(self, name, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.name = name
        self.setStyleSheet("QLineEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 14px;"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #a8a8a8"
                "}"
                "QLineEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QLineEdit:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        self.textChanged.connect(self.changeValue)

    @pyqtSlot(str)
    def changeValue(self, text):
        if text == '':
            text = '{' + self.name + '}'
        self.ValueChanged.emit(self.name, text, "text")
    
class OkDatetimeEdit(QtGui.QDateTimeEdit):
    ValueChanged = pyqtSignal(str, str, str)
    def __init__(self, name, parent=None):
        QtGui.QDateTimeEdit.__init__(self, parent)
        self.name = name
        self.setStyleSheet("QDateTimeEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 18px;"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #a8a8a8"
                "}"
                "QDateTimeEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QDateTimeEdit:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        calendar = QtGui.QCalendarWidget()
        self.setDateTime(QtCore.QDateTime.currentDateTime())
        self.setCalendarPopup(True)
        self.setCalendarWidget(calendar)
        self.dateTimeChanged.connect(self.changeValue)
        
    @pyqtSlot(QtCore.QDateTime)
    def changeValue(self, datetime):
        self.ValueChanged.emit(self.name, datetime.toString("yyyy-MM-dd hh:mm:ss"), "datetime")
        
class OkIncrementEdit(OkTextEdit):
    def __init__(self, name, parent=None):
        OkTextEdit.__init__(self, name, parent)
