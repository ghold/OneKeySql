from PyQt4 import QtGui
from xml.sax import parse

class OkModel(QtGui.QStandardItemModel):
    data = []
    
    def __init__(self,  file, handler, parent = None):
        QtGui.QStandardItemModel.__init__(self,  parent)
        self.appendRow(QtGui.QStandardItem(file))
        self.handler = handler()
        parse(file, self.handler)
        self.data = self.handler.getXmlData()
        self.setupModel(self.data, self.item(0))
        
    def setupModel(self, t_data,  t_item):
        for key,  val in t_data.items():
            item = QtGui.QStandardItem(key)
            t_item.appendRow(item)
            item.setData(val)
            if isinstance(val, dict):
                self.setupModel(val, item)
