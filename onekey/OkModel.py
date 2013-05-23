from PyQt4 import QtGui, Qt
from OkListItem import OkListItem
from xml.sax import parse
from OkListWidget import *
from OkListItem import OkAddonWidget

class OkModel(object):
    data = []
    
    def __init__(self,  file, handler, parent = None):
        self.handler = handler()
        parse(file, self.handler)
        self.data = self.handler.getXmlData()
        
    def makeupTestList(self, type):
        #self.test_list = OkCaseWidget() if type == "Case" else OkUnitWidget()
        self.test_list = OkCaseWidget()
        for key,  val in self.data.items():
            #print(val["data"]["name"])
            item = OkListItem(val["data"]["name"], self.test_list)
            item.setData(Qt.Qt.UserRole, val)
            self.test_list.addItem(item)
            self.test_list.setItemWidget(item, OkAddonWidget(val["data"]["desc"], item, self.test_list))
        return self.test_list
            
    def makeupStepList(self, item):
        self.step_list = OkListWidget()
        tmp_data = item.data(Qt.Qt.UserRole)
        step_count = len(tmp_data["data"]["steps"])
        for i in range(step_count):
            val = tmp_data["data"]["steps"][i]
            item = OkListItem("_".join((val["from"], val["type"], val["data_id"])), self.step_list)
            #print(item.text())
            item.setData(Qt.Qt.UserRole, val)
            self.step_list.addItem(item)
        return self.step_list
