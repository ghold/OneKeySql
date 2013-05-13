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
        name = args[0]
        return OkDatetimeEdit(name)
    @classmethod    
    def text(cls, *args):
        from OkEdit import OkTextEdit
        name = args[0]
        return OkTextEdit(name)
    @classmethod
    def datetime_arg(cls, *args):
        datetime, arg = args
        datetime = QtCore.QDateTime.fromString(datetime, Qt.Qt.ISODate)
        return datetime.addMSecs(float(arg) * 1000 * 60).toString(Qt.Qt.ISODate)

