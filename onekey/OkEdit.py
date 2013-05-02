from PyQt4 import QtCore, QtGui, Qt

class OkTextEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.setStyleSheet("QLineEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 18px;"
                    "padding-left:3px;"
                    "width:300px"
                "}"
                "QLineEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QLineEdit:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        
class OkDateTimeEdit(QtGui.QDateTimeEdit):
    def __init__(self, parent=None):
        QtGui.QDateTimeEdit.__init__(self, parent)
        self.setStyleSheet("QDateTimeEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 18px;"
                    "padding-left:3px;"
                    "width:300px"
                "}"
                "QDateTimeEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QDateTimeEdit:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        calendar = QtGui.QCalendarWidget()
        self.setCalendarWidget(calendar)
        self.setCalendarPopup(True)
