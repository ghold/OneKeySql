import argparse
from xml.sax import parse
import OkXmlHandler
from OkModel import OkModel
from OkConfig import OkConfig
import json
import re
from OkXmlHandler import OkTestcaseHandler

class OkDataParser(object):
    def __init__(self):
        self.cache = {}
        self.data = {}
        self.tag_position = {}
        self.config = OkConfig()
        
    def subTag(self, tags, data, spec):
        if spec:
            pass
        else:
            print("VALUES( ")
        tag_pattern = r'\{[0-9a-zA-Z_]+\((?P<name>[0-9a-zA-Z_]+)\)\}'
        tag_compiler =re.compile(tag_pattern)
        tag_list = tag_compiler.split(data)
        order = 0
        arg_pattern = r'\{(?P<name>[0-9a-zA-Z_]+)(?:|\((?P<arg>[+-]{1}[0-9]+)\))\}'
        arg_compiler = re.compile(arg_pattern)
        for val in tag_list:
            if tags.get(val) is not None:
                arg_match = arg_compiler.match(tags[val])
                if arg_match is not None:
                    self.tag_position.setdefault(arg_match.group("name"), [])
                    self.tag_position[arg_match.group("name")].append((order, arg_match.group("arg")))
                print(tags[val])
                order += 1
            else:
                print(val)
                
        if spec:
            print(";\n")
        else:
            print(");\n")
    
    #data setting
    def setupData(self, data):
        self.data = data
        for step in range(0, len(data)):
            
            key =  "%s_%s" %(data[step]["type"], data[step]["from"])
            model = self.cache.get(key)
            
            if  model is not None:
                pass
            else:
                xml_filename = "%s/%s.xml" % (data[step]["type"], data[step]["from"])
                handler_type = "Ok%sHandler" % data[step]["type"].capitalize()
                handler = getattr(OkXmlHandler, handler_type, None)
                model = OkModel((xml_filename, handler, 'unit'))
                self.cache[key] = model
            
            data_id = data[step]["type"] + "_" + data[step]["data_id"]
            step_data = model.data['unit'][data_id]["data"]
            
            #self.titleFormat(step + 1, step_data['desc'])
            
            if (step_data.get("table", None) is not None and step_data.get("column", None) is not None):
                tp_sql = "INSERT INTO\n%s(%s)\n" % (step_data["table"], step_data["column"])
                print(tp_sql)
                self.subTag(data[step]["tags"], step_data["value"], False)
            else:
                self.subTag(data[step]["tags"], step_data["value"], True)


def isArgSet(data, options):
    option_dict = {}
    if options is not None:
        for option in options:
            op = option.split(':')
            option_dict.setdefault(op[0].strip(), op[1].strip())
    
    need = []
    #match the form like {type_name(tag_name:default_val)}
    tag_pattern = r"\{([0-9a-zA-Z_]+)\((?P<name>[0-9a-zA-Z_]+)(?:|\:(?P<def>.+))\)(?:|(?P<view>!))\}"
    tag_compiler = re.compile(tag_pattern)
    
    for tag in data['data']['var'].split(','):
        result = tag_compiler.match(tag)
        tmp_default_value = result.group("def")
        name = result.group("name")
        
        if tmp_default_value is None:
            if option_dict.get(name, None) is None:
                need.append(name)
                
    return need


def init(id, option):
    print(option)
    handler = OkTestcaseHandler()
    parse('testcase/testcase.xml', handler)
    data = handler.getXmlData()
    parser = OkDataParser()
    key = "testcase_%s"%id
    
    need = isArgSet(data[key], option)
    if len(need) > 0:
        print("You need to add %s"%' '.join(need))
    
    #jsonDumpsIndentStr = json.dumps(data[key], indent=1)
    #print(jsonDumpsIndentStr)
    #parser.setupData(data[key]["data"]["steps"])
    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--id", type=str, help="testcase id")
    parser.add_argument("-o", "--option", type=str, help="options", nargs="*")
    
    args = parser.parse_args()
    init(args.id, args.option)
