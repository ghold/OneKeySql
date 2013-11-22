from PyQt4 import QtGui, QtCore, Qt
from OkXmlWriter import OkTestcaseWriter
import os

class OkBasket(QtGui.QListWidget):
    path =  os.environ['ONEKEY_HOME']
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
            writer = OkTestcaseWriter(self.path + '/testcase/testcase.xml')
            data = eval(bytes(event.mimeData().data('application/ok-case')).decode("utf-8"))
            writer.deleteCase(data["id"])
            self.topLevelWidget().openEditMode(self.topLevelWidget().caseList.selectedItem)
            self.topLevelWidget().caseList.topLevelItem(int(data["tl"])).takeChild(int(data["row"]))
            if self.topLevelWidget().caseList.topLevelItem(int(data["tl"])).childCount() == 0:
                self.topLevelWidget().caseList.takeTopLevelItem(int(data["tl"]))
            self.topLevelWidget().model.update()
            if self.topLevelWidget().mainSplitter.widget(1).widget(1) is not None:
                self.topLevelWidget().mainSplitter.widget(1).widget(1).setParent(None)
            event.accept()
        elif event.mimeData().hasFormat('application/ok-step'):
            event.setDropAction(QtCore.Qt.CopyAction)
            writer = OkTestcaseWriter(self.path + '/testcase/testcase.xml')
            row = bytes(event.mimeData().data('application/ok-step')).decode("utf-8")
            selectedItem = self.topLevelWidget().caseList.selectedItem
            parentId = selectedItem.data(0,Qt.Qt.UserRole)['id']
            writer.deleteLastStep(parentId)
            self.topLevelWidget().stepList.takeItem(int(row))
            self.topLevelWidget().model.update()
            self.topLevelWidget().model.updateCaseItem(selectedItem)
            event.accept()
        else:
            event.ignore()
