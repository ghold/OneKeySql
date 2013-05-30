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
        name, default = args
        return OkDatetimeEdit(name, default)
        
    @classmethod
    def date(cls, *args):
        from OkEdit import OkDateEdit
        name, default = args
        return OkDateEdit(name, default)
        
    @classmethod        
    def time(cls, *args):
        from OkEdit import OkTimeEdit
        name, default = args
        return OkTimeEdit(name, default)
        
    @classmethod    
    def text(cls, *args):
        from OkEdit import OkTextEdit
        name, default = args
        return OkTextEdit(name, default)
        
    @classmethod    
    def increment(cls, *args):
        from OkEdit import OkIncrementEdit
        name, default = args
        return OkIncrementEdit(name, default)
        
    @classmethod
    def datetime_arg(cls, *args):
        datetime, arg, default, config = args
        return QtCore.QDateTime.fromString(datetime, "yyyy-MM-dd hh:mm:ss").addMSecs(float(arg) * 1000 * 60).toString("yyyy-MM-dd hh:mm:ss")
        
    @classmethod
    def date_arg(cls, *args):
        date, arg, default, config = args
        return QtCore.QDate.fromString(date, "yyyy-MM-dd").addDays(int(arg)).toString("yyyy-MM-dd")
        
    @classmethod
    def time_arg(cls, *args):
        time, arg, default, config = args
        return QtCore.QTime.fromString(time, "hh:mm:ss").addMSecs(float(arg) * 1000 * 60).toString("hh:mm:ss")
        
    @classmethod    
    def increment_arg(cls, *args):
        number, arg, default, config = args
        try:
            if config.INCREMENT is None:
                config.INCREMENT = number
            config.INCREMENT = int(config.INCREMENT) + int(arg)
            setattr(config, default, "%d"%config.INCREMENT)
            return config.INCREMENT
        except ValueError:
            return number.strip("}") + "(" + arg + ")}"
    
