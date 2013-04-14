from xml.sax.handler import ContentHandler
from xml.sax import parse

class testunit_handler(ContentHandler):
    def __init__(self):
        self.data = []
        self.testunits = {}
        self.testunit_id = ''
        
    def startElement(self,  name,  attrs):
        if name == 'testunits':
            for key,  val in attrs.items():
                self.testunits[key] = val
            self.testunits['data'] = {}
        elif name == 'testunit':
            self.testunit_id = 'testunit_' + attrs['id']
            self.testunits['data'][self.testunit_id] = {}
            for key,  val in attrs.items():
                self.testunits['data'][self.testunit_id][key] = val
                self.testunits['data'][self.testunit_id]['data'] = {}
            
    def endElement(self,  name):
        if name != 'testunits' and name != 'testunit':
            self.testunits['data'][self.testunit_id]['data'][name] = self.data
            self.data = []
            
    def characters(self,  string):
        if string.strip() != '':
            self.data.append(string.strip())
            
test = testunit_handler()    
parse('sample.xml',  test)
print(test.testunits)
