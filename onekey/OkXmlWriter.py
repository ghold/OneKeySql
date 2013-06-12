from xml.etree.ElementTree import ElementTree, Element
from OkConfig import OkConfig

class OkTestcaseWriter(object):
    def __init__(self, file):
        self.tree = ElementTree()
        self.tree.parse(file)
        self.root = self.tree.getroot()
        self.config = OkConfig()
        
    def getMaxId(self):
        result = self.root.findall("./testcase")
        idList = []
        for val in result:
            idList.append(int(val.get("id")))
        return max(idList)
        
    def createCase(self, name, desc):
        #id
        id = self.getMaxId()
        id = "%.5d" % (id + 1)
        #case element
        element = Element('testcase', {"id":id})
        nameElement = Element('name')
        nameElement.text = name
        element.append(nameElement)
        descElement = Element('desc')
        descElement.text = desc
        element.append(descElement)
        varElement = Element('var')
        element.append(varElement)
        stepsElement = Element('steps')
        element.append(stepsElement)
        
        self.root.append(element)
        self.writeXml('testcase/testcase.xml')
        
    def makeupElement(self, data, id):
        #vars
        result = self.root.find("./testcase[@id='%s']/var"% id)
        if result.text is not None:
            varList = [i.strip() for i in result.text.split(',')]
        else:
            result.text = ''
            varList = []
        #step
        tags = data.pop('tags')
        element = Element('step', data)
        #tags
        for tag, val in tags.items():
            print(val)
            if val[0] == 2:
                if val[4] == 1:
                    for ind in range(len(varList)):
                        if varList[ind].find("{%s(%s:"%(val[5], val[1])) >= 0 or varList[ind].find("{%s(%s)"%(val[5], val[1])) >= 0:
                            varList[ind] = varList[ind].replace('!}','}')
                        result.text = ','.join(varList)
                        break
                if val[4] == 2:
                    for ind in range(len(varList)):
                        if varList[ind].find("{%s(%s:"%(val[5], val[1])) >= 0 or varList[ind].find("{%s(%s)"%(val[5], val[1])) >= 0:
                            varList[ind] = varList[ind].replace('}','!}')
                        result.text = ','.join(varList)
                        break
                tagElement = Element('tag', {'name':tag, 'type':("%d"%val[0])})
                if len(val[3]) > 0:
                    tagElement.text = "{%s(%s)}"%(val[1], val[3])
                elif val[5] == 'increment':
                    tagElement.text = "{%s(%s)}"%(val[1], '+0')
                else:
                    tagElement.text = "{%s}"% val[1]
                element.append(tagElement)
            elif val[0] == 1:
                if len(result.text)>0:
                    result.text = result.text + ','
                if val[2] is not None and len(val[2])>0:
                    if self.config.callback(val[2].upper()) is not None:
                        model = "{%s(%s:%s)!}"
                        if val[4]:
                            model = "{%s(%s:%s)}"
                        result.text = result.text + model%(val[5], val[1], val[2].upper())
                    else:
                        model = "{%s(%s:'%s')!}"
                        if val[4]:
                            model = "{%s(%s:'%s')}"
                        result.text = result.text + model%(val[5], val[1], val[2])
                else:
                    model = "{%s(%s)!}"
                    if val[4]:
                        model = "{%s(%s)}"
                    result.text = result.text + model%(val[5], val[1])
                    
                tagElement = Element('tag', {'name':tag, 'type':("%d"%val[0])})
                if val[3] is not None and len(val[3]) > 0:
                    tagElement.text = "{%s(%s)}"%(val[1], val[3])
                elif val[5] == 'increment':
                    tagElement.text = "{%s(%s)}"%(val[1], '+0')
                else:
                    tagElement.text = "{%s}"% val[1]
                element.append(tagElement)    
            else:
                tagElement = Element('tag', {'name':tag, 'type':("%d"%val[0])})
                tagElement.text = val[2]
                element.append(tagElement)
        result = self.root.find("./testcase[@id='%s']/steps"% id)
        result.append(element)
        self.writeXml('testcase/testcase.xml')
        
    def deleteCase(self, id):
        result = self.root.find("./testcase[@id='%s']"% id)
        self.root.remove(result)
        self.writeXml('testcase/testcase.xml')
        
    def writeXml(self, file):
        self.tree.write(file, encoding="UTF-8", xml_declaration=True, method='xml')

#wirter = OkTestcaseWriter('testcase/testcase.xml')
#wirter.AppendStepById("00001")
#wirter.writeXml('testcase/output.xml')
