from PyQt4 import Qt, QtCore, Qt
class OkScrollArea(Qt.QScrollArea):
    def __init__(self, parent=None):
        Qt.QScrollArea.__init__(self, parent)
        self.setVerticalScrollBar(OkScrollBar())
        self.setStyleSheet("QScrollArea{"
                    "border: 0px;"
                    "background: #323232;"
                "}")
        #self.setSizePolicy(Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)
        
class OkScrollBar(Qt.QScrollBar):
    def __init__(self, parent=None):
        Qt.QScrollBar.__init__(self, parent)
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
