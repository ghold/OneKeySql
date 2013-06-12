from PyQt4 import QtGui, QtCore, Qt
from OkXmlWriter import OkTestcaseWriter

class OkBasket(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setMaximumSize(50, 50)
        
        self.setStyleSheet("OkBasket{"
                    "border: 0px;"
                    "background: #eeeeee"
                "}")
        
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
                
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/ok-case') or event.mimeData().hasFormat('application/ok-step'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/ok-case') or event.mimeData().hasFormat('application/ok-step'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/ok-case'):
            event.setDropAction(QtCore.Qt.CopyAction)
            writer = OkTestcaseWriter('testcase/testcase.xml')
            data = eval(bytes(event.mimeData().data('application/ok-case')).decode("utf-8"))
            writer.deleteCase(data["id"])
            self.topLevelWidget().openEditMode(self.topLevelWidget().caseList.selectedItem)
            self.topLevelWidget().caseList.takeItem(int(data["row"]))
            self.topLevelWidget().model.update()
            if self.topLevelWidget().mainSplitter.widget(1).widget(1) is not None:
                self.topLevelWidget().mainSplitter.widget(1).widget(1).setParent(None)
            event.accept()
        elif event.mimeData().hasFormat('application/ok-step'):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
