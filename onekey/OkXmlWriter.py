from xml.etree.ElementTree import ElementTree, Element

class OkTestcaseWriter(object):
    def __init__(self, file):
        self.tree = ElementTree()
        self.tree.parse(file)
        self.root = self.tree.getroot()
        
    def AppendVarById(self, id, var):
        result = self.root.find("./testcase[@id='%s']/var"% id)
        result.text = result.text + ',' + var
        
    def AppendStepById(self, id):
        result = self.root.find("./testcase[@id='%s']/steps"% id)
        element = Element('step', {'hello':'123'})
        result.append(element)
        
    def makeupData(self, data):
        tags = data.pop('tags')
        self.element = Element('step', data)
        for tag, val in tags.items():
            print(val)
    
    def writeXml(self, file):
        self.tree.write(file, encoding="UTF-8")

wirter = OkTestcaseWriter('testcase/testcase.xml')
wirter.AppendStepById("00001")
wirter.writeXml('testcase/output.xml')
