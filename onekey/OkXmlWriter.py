from xml.etree.ElementTree import ElementTree, Element
from OkConfig import OkConfig
import os

class OkTestcaseWriter(object):
    path =  os.environ['ONEKEY4499_HOME']
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
        if len(idList) == 0:
            return 0
        return max(idList)

    def createCase(self, name, cate, desc):
        #id
        id = self.getMaxId()
        id = "%.5d" % (id + 1)
        #case element
        element = Element('testcase', {"id":id})
        nameElement = Element('name')
        nameElement.text = name
        element.append(nameElement)
        cateElement = Element('cate')
        cateElement.text = cate
        element.append(cateElement)
        descElement = Element('desc')
        descElement.text = desc
        element.append(descElement)
        varElement = Element('var')
        element.append(varElement)
        stepsElement = Element('steps')
        element.append(stepsElement)
        
        self.root.append(element)
        self.writeXml(self.path + '/testcase/testcase.xml')
        
    def makeupElement(self, data, id):
        #vars
        result = self.root.find("./testcase[@id='%s']/var"% id)
        varList = []
        if result.text is not None:
            varList = [i.strip() for i in result.text.split(',')]
        else:
            result.text = ''
        #usedVarList
        usedVarItem = {}
        #step
        tags = data.pop('tags')
        element = Element('step', data)
        #tags
        for tag, val in tags.items():
            if val[0] == 2:
                usedVarItem[tag] = val
            elif val[0] == 1:
                if val[2] is not None and len(val[2])>0:
                    if self.config.callback(val[2].upper()) is not None:
                        model = "{%s(%s:%s)!}"
                        if val[4]:
                            model = "{%s(%s:%s)}"
                        varList.append(model%(val[5], val[1], val[2].upper()))
                    else:
                        model = "{%s(%s:'%s')!}"
                        if val[4]:
                            model = "{%s(%s:'%s')}"
                        varList.append(model%(val[5], val[1], val[2]))
                else:
                    model = "{%s(%s)!}"
                    if val[4]:
                        model = "{%s(%s)}"
                    varList.append(model%(val[5], val[1]))
                    
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
        result.text = ','.join(varList)
        for tag, val in usedVarItem.items():
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
            if val[3] is not None and len(val[3]) > 0:
                tagElement.text = "{%s(%s)}"%(val[1], val[3])
            elif val[5] == 'increment':
                tagElement.text = "{%s(%s)}"%(val[1], '+0')
            else:
                tagElement.text = "{%s}"% val[1]
            element.append(tagElement)
                
        result = self.root.find("./testcase[@id='%s']/steps"% id)
        result.append(element)
        self.writeXml(self.path + '/testcase/testcase.xml')
        
    def deleteCase(self, id):
        result = self.root.find("./testcase[@id='%s']"% id)
        self.root.remove(result)
        self.writeXml(self.path + '/testcase/testcase.xml')
        
    def deleteLastStep(self, id):
        case = self.root.find("./testcase[@id='%s']"% id)
        varEle = case.find("./var")
        steps = case.find("./steps")
        lastStep = steps.find("./step[last()]")
        tags = lastStep.findall("./tag")
        
        varList = []
        if varEle.text is not None:
            varList = [i.strip() for i in varEle.text.split(',')]
        else:
            varEle.text = ''
        
        for item in tags:
            if item.get("type") == "1":
                tag_hasArg = "(%s:" % item.text.strip('{} ').split('(')[0]
                tag_noArg = "(%s)" % item.text.strip('{} ').split('(')[0]
                for var in varList:
                    if tag_hasArg in var or tag_noArg in var:
                        varList.remove(var)
                        break
                        
        varEle.text = ','.join(varList)
        
        steps.remove(lastStep)
        self.writeXml(self.path + '/testcase/testcase.xml')
        
    def writeXml(self, file):
        self.tree.write(file, encoding="UTF-8", xml_declaration=True, method='xml')

#wirter = OkTestcaseWriter('testcase/testcase.xml')
#wirter.AppendStepById("00001")
#wirter.writeXml('testcase/output.xml')
