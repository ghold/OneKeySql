from xml.etree.ElementTree import ElementTree, Element
from OkConfig import OkConfig

class OkTestcaseWriter(object):
    def __init__(self, file):
        self.tree = ElementTree()
        self.tree.parse(file)
        self.root = self.tree.getroot()
        self.config = OkConfig()
        
    def appendStepById(self, id):
        result = self.root.find("./testcase[@id='%s']/steps"% id)
        element = Element('step', {'hello':'123'})
        result.append(element)
        
    def makeupElement(self, data, id):
        #vars
        result = self.root.find("./testcase[@id='%s']/var"% id)
        varList = [i.strip() for i in result.text.split(',')]
        #step
        tags = data.pop('tags')
        self.element = Element('step', data)
        #tags
        for tag, val in tags.items():
            if val[0] == 2:
                if val[4] == 1:
                    for id in range(len(varList)):
                        if varList[id].find("{%s(%s:"%(val[5], val[1])) >= 0 or varList[id].find("{%s(%s)"%(val[5], val[1])) >= 0:
                            varList[id] = varList[id].replace('!}','}')
                        result.text = ','.join(varList)
                        break
                if val[4] == 2:
                    for id in range(len(varList)):
                        if varList[id].find("{%s(%s:"%(val[5], val[1])) >= 0 or varList[id].find("{%s(%s)"%(val[5], val[1])) >= 0:
                            varList[id] = varList[id].replace('}','!}')
                        result.text = ','.join(varList)
                        break
                tagElement = Element('tag', {'name':tag})
                if len(val[3]) > 0:
                    tagElement.text = "{%s(%s)}"%(val[1], val[3])
                elif val[5] == 'increment':
                    tagElement.text = "{%s(%s)}"%(val[1], '+0')
                else:
                    tagElement.text = "{%s}"% val[1]
                self.element.append(tagElement)
            elif val[0] == 1:
                if val[2] is not None and len(val[2])>0:
                    if self.config.callback(val[2].upper()) is not None:
                        model = ",{%s(%s:%s)!}"
                        if val[4]:
                            model = ",{%s(%s:%s)}"
                        result.text = result.text + model%(val[5], val[1], val[2].upper())
                    else:
                        print(val[2])
                        model = ",{%s(%s:'%s')!}"
                        if val[4]:
                            model = ",{%s(%s:'%s')}"
                        result.text = result.text + model%(val[5], val[1], val[2])
                else:
                    model = ",{%s(%s)!}"
                    if val[4]:
                        model = ",{%s(%s)}"
                    result.text = result.text + model%(val[5], val[1])
                    
                tagElement = Element('tag', {'name':tag})
                if val[3] is not None and len(val[3]) > 0:
                    tagElement.text = "{%s(%s)}"%(val[1], val[3])
                elif val[5] == 'increment':
                    tagElement.text = "{%s(%s)}"%(val[1], '+0')
                else:
                    tagElement.text = "{%s}"% val[1]
                self.element.append(tagElement)    
            else:
                tagElement = Element('tag', {'name':tag})
                tagElement.text = val[2]
                self.element.append(tagElement)
        result = self.root.find("./testcase[@id='%s']/steps"% id)
        result.append(self.element)
        self.writeXml('testcase/output.xml')
        
    
    def writeXml(self, file):
        self.tree.write(file, encoding="UTF-8")

#wirter = OkTestcaseWriter('testcase/testcase.xml')
#wirter.AppendStepById("00001")
#wirter.writeXml('testcase/output.xml')
