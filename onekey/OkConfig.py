from configparser import ConfigParser
from PyQt4 import QtGui, QtCore

class OkConfigHandler(object):
    #date
    TODAY = QtCore.QDate.currentDate()
    YESTERDAY = TODAY.addDays(-1)
    
    #datetime
    CURRENT_TM = QtCore.QDateTime.currentDateTime()
    
    def callback(self,  name,  *args):
        method = getattr(self,  name,  None)
        if callable(method):
            return method(*args)
        return method
    
    def __init__(self):
        self.config = ConfigParser()
        self.config.read_file(open("config.conf"))
        for section in self.config.sections():
            for val in self.config.items(section):
                setattr(self, val[0].upper(), val[1])
                
    def parse(self):
        pass
if __name__ == "__main__":
    hello = OkConfigHandler()
    print(hello.callback("BAR_RECORD_ID"))
