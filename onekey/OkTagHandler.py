from PyQt4 import QtGui
from OkEdit import *
from OkLabel import OkLabel

class OKTagWidget(QtGui.Widget):
    def __init__(self, name, type, parent=None):
        QtGui.Widget.__init__(self, parent)
        #type
        type_name = "Ok" + type.capitalize() + "Edit"
        type_class = getattr(OkEdit, type_name, None)
        if callable(method):
            self.type_widget = type_class()
            
        self.label = OkLabel(name)        
        
class OKTagHandler(object):
    def callback(self,  name,  *args):
        method = getattr(self,  name,  None) 
        if callable(method):
            return method(*args)
            
    def datetime(self, *args):
        arg = args
        return 

