from PyQt4 import Qt
from OkListItem import OkListItem
from xml.sax import parse
from OkListWidget import *
from OkListItem import *

class OkModel(object):
    def __init__(self,  *args):
        self.data = {}
        if len(args) > 0:
            self.args = args
        for val in self.args:
            handler = val[1]()
            parse(val[0], handler)
            if self.data.get(val[2]) is None:
                self.data[val[2]] = []
            self.data[val[2]] = handler.getXmlData()
            
    def update(self):
        self.__init__()
        
    def makeupExecList(self):
        self.test_list = OkCaseWidget()
        for key,  val in self.data['case'].items():
            item = OkListItem(val["data"]["name"], self.test_list)
            item.setData(Qt.Qt.UserRole, val)
            self.test_list.addItem(item)
            self.test_list.setItemWidget(item, OkExecAddon(val["data"]["desc"], item, self.test_list))
        return self.test_list
        
    def makeupCaseList(self):
        self.test_list = OkCaseWidget()
        for key,  val in self.data['case'].items():
            item = OkListItem(val["data"]["name"], self.test_list)
            item.setData(Qt.Qt.UserRole, val)
            self.test_list.addItem(item)
            self.test_list.setItemWidget(item, OkCaseAddon(val["data"]["desc"], item, self.test_list))
        return self.test_list
        
    def makeupUnitList(self):
        self.test_list = OkUnitWidget()
        for key,  val in self.data['unit'].items():
            item = OkListItem(val["data"]["name"], self.test_list)
            item.setData(Qt.Qt.UserRole, val)
            self.test_list.addItem(item)
        return self.test_list
            
    def makeupStepList(self, item):
        self.step_list = OkStepWidget(item)
        tmp_data = item.data(Qt.Qt.UserRole)
        step_count = len(tmp_data["data"]["steps"])
        for i in range(step_count):
            val = tmp_data["data"]["steps"][i]
            name = self.data['unit']['testunit_'+ val["data_id"]]['data']['name']
            item = OkListItem(name, self.step_list)
            item.setData(Qt.Qt.UserRole, val)
            self.step_list.addItem(item)
        return self.step_list
