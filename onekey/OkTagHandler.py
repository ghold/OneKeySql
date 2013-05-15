from PyQt4 import QtCore, QtGui, Qt
class OkTagHandler(object):
    @classmethod
    def callback(cls,  name,  *args):
        method = getattr(cls,  name,  None)
        if callable(method):
            return method(*args)
            
    @classmethod        
    def datetime(cls, *args):
        from OkEdit import OkDatetimeEdit
        name, defualt = args
        return OkDatetimeEdit(name)
        
    @classmethod    
    def text(cls, *args):
        from OkEdit import OkTextEdit
        name, defualt = args
        return OkTextEdit(name)
        
    @classmethod    
    def increment(cls, *args):
        from OkEdit import OkIncrementEdit
        name, defualt = args
        return OkIncrementEdit(name)
        
    @classmethod
    def datetime_arg(cls, *args):
        datetime, arg = args
        datetime = QtCore.QDateTime.fromString(datetime, Qt.Qt.ISODate)
        return datetime.addMSecs(float(arg) * 1000 * 60).toString("yyyy-MM-dd hh:mm:ss")
    
