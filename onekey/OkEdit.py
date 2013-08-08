from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import pyqtSignal, pyqtSlot

class OkTextEdit(QtGui.QLineEdit):
    #define ValueChanged Signal
    ValueChanged = pyqtSignal(str, str, str, str)
    def __init__(self, name=None, default=None, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.name = name
        self.default = default
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
        
    def setValue(self, text):
        self.setText(text)
        
    def getValue(self):
        return self.text()

    @pyqtSlot(str)
    def changeValue(self, text):
        if self.name is None:
            return
        if text == '':
            text = '{' + self.name + '}'
        #send the singal
        self.ValueChanged.emit(self.name, text, "text", self.default)

class OkMinuteEdit(OkTextEdit):
    def __init__(self, name=None, default=None, parent=None):
        OkTextEdit.__init__(self, name, default, parent)
    
    @pyqtSlot(str)
    def changeValue(self, text):
        if self.name is None:
            return
        if text == '':
            text = '{' + self.name + '}'
        self.ValueChanged.emit(self.name, '%d'%(int(text)), "minute", self.default)
        
class OkIncrementEdit(OkTextEdit):
    def __init__(self, name=None, default=None, parent=None):
        OkTextEdit.__init__(self, name, default, parent)
        
    @pyqtSlot(str)
    def changeValue(self, text):
        if self.name is None:
            return
        if text == '':
            text = '{' + self.name + '}'
        self.ValueChanged.emit(self.name, text, "increment", self.default)

class OkDatetimeEdit(QtGui.QDateTimeEdit):
    ValueChanged = pyqtSignal(str, str, str, str)
    def __init__(self, name=None, default=None, parent=None):
        QtGui.QDateTimeEdit.__init__(self, parent)
        self.name = name
        self.default = default
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
        #calendar = QtGui.QCalendarWidget()
        self.setCalendarPopup(False)
        #self.setCalendarWidget(calendar)
        self.dateTimeChanged.connect(self.changeValue)
        
    def setValue(self, datetime):
        self.setDateTime(QtCore.QDateTime.fromString(datetime, "yyyy-MM-dd hh:mm:ss"))
        
    def getValue(self):
        return self.dateTime().toString("yyyy-MM-dd hh:mm:ss")

    @pyqtSlot(QtCore.QDateTime)
    def changeValue(self, datetime):
        if self.name is None:
            return
        self.ValueChanged.emit(self.name, datetime.toString("yyyy-MM-dd hh:mm:ss"), "datetime", self.default)
        
class OkDateEdit(QtGui.QDateEdit):
    ValueChanged = pyqtSignal(str, str, str, str)
    def __init__(self, name=None, default=None, parent=None):
        QtGui.QDateEdit.__init__(self, parent)
        self.name = name
        self.default = default
        self.setStyleSheet("QDateEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 18px;"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #a8a8a8"
                "}"
                "QDateEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QDateEdit:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        #calendar = QtGui.QCalendarWidget()
        #self.setDate(QtCore.QDate.currentDate())
        self.setCalendarPopup(False)
        #self.setCalendarWidget(calendar)
        self.dateChanged.connect(self.changeValue)
        
    def setValue(self, date):
        self.setDate(QtCore.QDate.fromString(date, "yyyy-MM-dd"))
        
    def getValue(self):
        return self.date().toString("yyyy-MM-dd")
        
    @pyqtSlot(QtCore.QDate)
    def changeValue(self, date):
        if self.name is None:
            return
        self.ValueChanged.emit(self.name, date.toString("yyyy-MM-dd"), "date", self.default )
        
class OkTimeEdit(QtGui.QTimeEdit):
    ValueChanged = pyqtSignal(str, str, str, str)
    def __init__(self, name=None, default=None, parent=None):
        QtGui.QTimeEdit.__init__(self, parent)
        self.name = name
        self.default = default
        self.setStyleSheet("QTimeEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 18px;"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #a8a8a8"
                "}"
                "QTimeEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QTimeEdit:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        #self.setDate(QtCore.QDate.currentDate())
        self.timeChanged.connect(self.changeValue)
        
    def setValue(self, time):
        self.setTime(QtCore.QTime.fromString(time, "hh:mm:ss"))
        
    def getValue(self):
        return self.time().toString("hh:mm:ss")
        
    @pyqtSlot(QtCore.QTime)
    def changeValue(self, time):
        if self.name is None:
            return
        self.ValueChanged.emit(self.name, time.toString("hh:mm:ss"), "time", self.default)
