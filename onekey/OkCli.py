import argparse
from xml.sax import parse
import OkXmlHandler
from OkModel import OkModel
from OkConfig import OkConfig
from OkTagHandlerCli import OkTagHandler
#import json
import re
import os
import multiprocessing
from OkXmlHandler import OkTestcaseHandler
from OkRuntime import OkExecProcess

class OkDataParser(object):
    def __init__(self):
        self.cache = {}
        self.sql = []
        self.data = {}
        self.result = {}
        self.config = OkConfig()
        
    def subTag(self, tags, data, result, spec):
        option = result["option"]
        var = result["var"]
        if spec:
            pass
        else:
            self.sql.append("VALUES( ")
            #print("VALUES( ")
        tag_pattern = r'\{[0-9a-zA-Z_]+\((?P<name>[0-9a-zA-Z_]+)\)\}'
        tag_compiler =re.compile(tag_pattern)
        tag_list = tag_compiler.split(data)
        arg_pattern = r'\{(?P<name>[0-9a-zA-Z_]+)(?:|\((?P<arg>[+-]{1}[0-9]+)\))\}'
        arg_compiler = re.compile(arg_pattern)
        for val in tag_list:
            if tags.get(val) is not None:
                arg_match = arg_compiler.match(tags[val])
                if arg_match is not None:
                    name = arg_match.group("name")
                    arg = arg_match.group("arg")
                    value = self.config.callback(var[name][1])
                    if value is not None:
                        if arg is not None:
                            method = var[name][0] + "_arg"
                            value = OkTagHandler.callback(method, value, arg, var[name][1], self.config)
                            self.config.reset()
                            #print(value)
                        self.sql.append(value)
                    if option.get(name, None) is not None and var[name][2] is None:
                        self.sql.append(option[name])
                        #print(option[name])
                else:
                    self.sql.append(tags[val])
                    #print(tags[val])
            else:
                self.sql.append(val)
                #print(val)
                
        if spec:
            self.sql.append(";\n")
            #print(";\n")
        else:
            self.sql.append(");\n")
            #print(");\n")
    
    #data setting
    def setupData(self, data, result):
        self.data = data
        self.result = result
        for step in range(0, len(data)):
            
            key =  "%s_%s" %(data[step]["type"], data[step]["from"])
            model = self.cache.get(key)
            
            if model is not None:
                pass
            else:
                xml_filename = "%s/%s.xml" % (data[step]["type"], data[step]["from"])
                handler_type = "Ok%sHandler" % data[step]["type"].capitalize()
                handler = getattr(OkXmlHandler, handler_type, None)
                model = OkModel((xml_filename, handler, 'unit'))
                self.cache[key] = model
            
            data_id = data[step]["type"] + "_" + data[step]["data_id"]
            step_data = model.data['unit'][data_id]["data"]
            
            self.sql.append("/*Step %d：%s*/\n" % (step + 1, step_data['desc']))
            
            if (step_data.get("table", None) is not None and step_data.get("column", None) is not None):
                tp_sql = "INSERT INTO\n%s(%s)\n" % (step_data["table"], step_data["column"])
                #print(tp_sql)
                self.sql.append(tp_sql)
                self.subTag(data[step]["tags"], step_data["value"], result, False)
            else:
                self.subTag(data[step]["tags"], step_data["value"], result, True)
                
    def getSql(self):
        return self.sql
        
    def sqlExec(self, data, result):
        self.setupData(data, result)
        thread = OkExecProcess(''.join(self.sql))
        thread.start()
        self.config.save()


def isArgSet(data, options):
    option_dict = {}
    if options is not None:
        for option in options:
            op = option.split(':')
            option_dict.setdefault(op[0].strip(), op[1].strip())
    
    need = []
    var = {}
    #match the form like {type_name(tag_name:default_val)}
    tag_pattern = r"\{(?P<type>[0-9a-zA-Z_]+)\((?P<name>[0-9a-zA-Z_]+)(?:|\:(?P<def>.+))\)(?:|(?P<view>!))\}"
    tag_compiler = re.compile(tag_pattern)
    
    for tag in data['data']['var'].split(','):
        result = tag_compiler.match(tag)
        var.setdefault(result.group("name"), (result.group("type"), result.group("def"), result.group("view")))
        tmp_default_value = result.group("def")
        name = result.group("name")
        
        if tmp_default_value is None:
            if option_dict.get(name, None) is None:
                need.append(name)
    
    return {"need":need, "var":var, "option":option_dict}


def init(id, option):
    handler = OkTestcaseHandler()
    path =  os.environ['ONEKEY_HOME']
    parse(path + '/testcase/testcase.xml', handler)
    data = handler.getXmlData()
    parser = OkDataParser()
    key = "testcase_%s"%id
    
    result = isArgSet(data[key], option)
    if len(result["need"]) > 0:
        print("You need to add %s. Formatted as -o %s"%(' '.join(result["need"]), ','.join([s+':'+s.upper() for s in result["need"]])))
        return
    
    #jsonDumpsIndentStr = json.dumps(data[key]["data"], indent=1)
    #print(jsonDumpsIndentStr)
    parser.sqlExec(data[key]["data"]["steps"], result)
    
if __name__ == "__main__":
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--id", type=str, help="testcase id")
    parser.add_argument("-o", "--option", type=str, help="options", nargs="*")
    
    args = parser.parse_args()
    init(args.id, args.option)
