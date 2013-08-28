from PyQt4 import Qt
from OkListItem import OkListItem
from xml.sax import parse
from OkListWidget import *
from OkListItem import *
from OkTreeWidget import *
from OkTreeItem import *
#from OkXmlHandler import OkTestcaseHandler, OkTestunitHandler
#import json

class OkModel(object):
    def __init__(self,  *args):
        self.data = {}
        if len(args) > 0:
            self.args = args
        for val in self.args:
            handler = val[1]()
            parse(val[0], handler)
            if self.data.get(val[2]) is None:
                self.data[val[2]] = {}
            self.data[val[2]].update(handler.getXmlData())
            
    def update(self):
        self.__init__()
        
    def makeupExecList(self):
        self.exec_list = OkCaseWidget()
        for key,  val in self.data['case'].items():
            item = OkListItem("%s_%s"%(val["id"], val["data"]["name"]), self.exec_list)
            item.setData(Qt.Qt.UserRole, val)
            self.exec_list.addItem(item)
            self.exec_list.setItemWidget(item, OkExecAddon(val["data"]["desc"], item, self.exec_list))
        return self.exec_list
        
#    def makeupCaseList(self):
#        self.case_list = OkCaseWidget()
#        for key,  val in self.data['case'].items():
#            item = OkListItem("%s_%s"%(val["id"], val["data"]["name"]), self.case_list)
#            item.setData(Qt.Qt.UserRole, val)
#            self.case_list.addItem(item)
#            self.case_list.setItemWidget(item, OkCaseAddon(val["data"]["desc"], item, self.case_list))
#        return self.case_list

    def makeupCaseList(self):
        self.case_list = OkCaseTreeWidget()
        for key,  val in self.data['case'].items():
            parent_item_list = self.case_list.findItems(val["data"]["cate"], Qt.Qt.MatchExactly)

            if len(parent_item_list) == 0:
                parent_item = OkTreeItem(val["data"]["cate"], self.case_list)
            else:
                parent_item = parent_item_list[0]

            item = OkTreeItem("%s_%s"%(val["id"], val["data"]["name"]), parent_item)
            item.setData(0, Qt.Qt.UserRole, val)
#            item.setData(Qt.Qt.UserRole, val)
#            self.case_list.addItem(item)
#            self.case_list.setItemWidget(item, OkCaseAddon(val["data"]["desc"], item, self.case_list))
        return self.case_list
        
    def makeupUnitList(self):
        self.unit_list = OkUnitWidget()
        for key,  val in self.data['unit'].items():
            item = OkListItem("%s_%s"%(val["id"], val["data"]["name"]), self.unit_list)
            item.setData(Qt.Qt.UserRole, val)
            self.unit_list.addItem(item)
        return self.unit_list
            
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
        
    def updateCaseItem(self, item):
        data = item.data(Qt.Qt.UserRole)
        key = "testcase_%s" % data['id']
        item.setData(Qt.Qt.UserRole, self.data['case'][key])

#model = OkModel(("testcase/testcase.xml", OkTestcaseHandler, 'case'),
#                ("testunit/testunit.xml", OkTestunitHandler, 'unit'), 
#                ("testunit/spec.xml", OkTestunitHandler, 'unit'))
#jsonDumpsIndentStr = json.dumps(model.data, indent=1)
#print(jsonDumpsIndentStr)
