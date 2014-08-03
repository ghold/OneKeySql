from PyQt4 import Qt

class OkSplitter(Qt.QSplitter):
    def __init__(self, parent=None):
        Qt.QSplitter.__init__(self, parent)
        self.setHandleWidth(1)
        self.setChildrenCollapsible(False)
        
        self.setStyleSheet("QSplitter::handle{"
                    "border: 0px;"
                    "color: #fff;"
                "}"
                "QSplitter{"
                    "border: 0px;"
                    "background-color: #fff;"
                "}")
