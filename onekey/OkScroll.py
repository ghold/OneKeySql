from PyQt4 import QtGui, QtCore, Qt
class OkScrollArea(QtGui.QScrollArea):
    def __init__(self, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
        self.setVerticalScrollBar(OkScrollBar())
        self.setStyleSheet("QScrollArea{"
                    "border: 0px;"
                    "background: #323232;"
                "}")
        #self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        
class OkScrollBar(QtGui.QScrollBar):
    def __init__(self, parent=None):
        QtGui.QScrollBar.__init__(self, parent)
        self.setStyleSheet("QScrollBar:vertical {"
                    "border:0px solid #ebece4;"
                    "width: 5px;"
                "}"
                " QScrollBar::handle:vertical {"
                    " background: grey;"
                    " min-height: 10px;"
                " }"
                " QScrollBar::add-line:vertical {"
                    " height: 0px;"
                    " subcontrol-position: bottom;"
                " }"
                " QScrollBar::sub-line:vertical {"
                    " height: 0px;"
                    " subcontrol-position: top;"
                " }"
                "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {"
                    " background: none;"
                "}"
                )