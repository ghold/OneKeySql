from configparser import ConfigParser
from PyQt4 import QtGui, QtCore

class OkConfigHandler(object):
    #date
    TODAY = QtCore.QDate.currentDate()
    YESTERDAY = TODAY.addDays(-1)
    
    #datetime
    CURRENT_TM = QtCore.QDateTime.currentDateTime()
    
    @classmethod
    def callback(cls,  name,  *args):
        cls.parse()
        method = getattr(cls,  name,  None)
        if callable(method):
            return method(*args)
        return method
    
    @classmethod
    def parse(cls):
        config = ConfigParser()
        config.read_file(open("config.conf"))
        for section in config.sections():
            default = config.get(section, "default")
            if config.has_option(section, "type") and config.get(section, "type") == "INCREMENT":
                setattr(cls, section, cls.generate_inits(default))
            else:
                setattr(cls, section, default)
        
    @classmethod
    def generate_inits(cls, N):
        for i in range(100):
            yield int(N)+1
        
if __name__ == "__main__":
    print(OkConfigHandler.callback("BAR_RECORD_ID"))
