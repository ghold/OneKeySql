from PyQt4 import QtGui
from xml.sax import parse

class OkModel(QtGui.QStandardItemModel):
    data = []
    
    def __init__(self,  file, handler, parent = None):
        QtGui.QStandardItemModel.__init__(self,  parent)
        self.parentItem = self.invisibleRootItem()
        self.handler = handler()
        parse(file, self.handler)
        self.data = self.handler.getXmlData()
        self.setupModel(self.data, self.parentItem)
        
    def setupModel(self, tmpData,  tmpItem):
        for key,  val in tmpData.items():
            item = QtGui.QStandardItem(key)
            tmpItem.appendRow(item)
            item.setData(val)
            if isinstance(val, dict):
                self.setupModel(val, item)
            
#if __name__ == '__main__':
#    test = OkTestCaseModel("testcase.xml")
#   print(test.invisibleRootItem().child(0).text())
