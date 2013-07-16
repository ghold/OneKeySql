from xml.sax.handler import ContentHandler
#from xml.sax import parse
#import json

class OkTestunitHandler(ContentHandler):
    def __init__(self):
        self.data = ''
        self.testunits = {}
        self.testunit_id = ''
        self.prifix = ''
        
    def startElement(self, name, attrs):
        if name == 'testunit':
            self.testunit_id = 'testunit_' + attrs['id']
            self.testunits[self.testunit_id] = {}
            for key,  val in attrs.items():
                self.testunits[self.testunit_id][key] = val
            self.testunits[self.testunit_id]['data'] = {}
            
    def endElement(self,  name):
        if name != 'testunits' and name != 'testunit':
            self.testunits[self.testunit_id]['data'][name] = self.data
            self.data = ''
            
    def characters(self,  string):
        if string.strip() != '':
            self.data = string.strip()
            
    def getXmlData(self):
        return self.testunits
        
class OkTestcaseHandler(ContentHandler):
    def __init__(self):
        self.data = ''
        self.testcases = {}
        self.testcase_id = ''
        self.step = 0
        self.tagname = ''
        
    def startElement(self,  name,  attrs):
        if name == 'testcase':
            self.step = 0
            self.testcase_id = 'testcase_' + attrs['id']
            self.testcases[self.testcase_id] = {}
            for key,  val in attrs.items():
                self.testcases[self.testcase_id][key] = val
            self.testcases[self.testcase_id]['data'] = {}
        elif name == 'steps':
            self.testcases[self.testcase_id]['data']['steps'] = {}
        elif name == 'step':
            self.testcases[self.testcase_id]['data']['steps'][self.step] = {}
            for key,  val in attrs.items():
                self.testcases[self.testcase_id]['data']['steps'][self.step][key] = val
            self.testcases[self.testcase_id]['data']['steps'][self.step]['tags'] = {}
            self.testcases[self.testcase_id]['data']['steps'][self.step]['tag_type'] = {}
        elif name == 'tag':
            self.tagname = attrs['name']
            self.tagtype = attrs['type']
                        
    def endElement(self,  name):
        if name == 'tag':
            self.testcases[self.testcase_id]['data']['steps'][self.step]['tags'][self.tagname] = self.data
            self.testcases[self.testcase_id]['data']['steps'][self.step]['tag_type'][self.tagname] = self.tagtype
        elif name == 'name' or name == 'desc'or name == 'var':
            self.testcases[self.testcase_id]['data'][name] = self.data
        elif name == 'step':
            self.step += 1
        self.data = ''
        
    def characters(self,  string):
        if string.strip() != '':
            self.data = string.strip()
            
    def getXmlData(self):
        return self.testcases

#test = OkTestunitHandler()
#parse('testunit/spec.xml', test)
#jsonDumpsIndentStr = json.dumps(test.getXmlData(), indent=1)
#print(jsonDumpsIndentStr)
