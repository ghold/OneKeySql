from PyQt4 import QtGui
class OKTagWidget(QtGui.Widget):
    def __init__(self, name, type, parent=None):
        QtGui.Widget.__init__(self, parent)
        tagLabel = QtGui.
        
class OKTagHandler(object):
    def callback(self,  name,  *args):
        method = getattr(self,  name,  None) 
        if callable(method):
            return method(*args)
            
    def date(self, name):
        

