from configparser import ConfigParser
from PyQt4 import QtGui, QtCore

class OkConfig(object):
    #date
    TODAY = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
    YESTERDAY = QtCore.QDate.currentDate().addDays(-1).toString("yyyy-MM-dd")
    
    #datetime
    CURRENT_TM = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
    
    #increment
    INCREMENT = None
    
    def callback(self,  name,  *args):
        if name is None:
            return None
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
                
    def reset(self):
        self.INCREMENT = None
        
    def save(self):
        for section in self.config.sections():
            for val in self.config.items(section):
                self.config.set(section, val[0], self.callback(val[0].upper()))
        self.config.write(open("config.conf", "w"))

if __name__ == "__main__":
    hello = OkConfig()
    print(hello.callback("BAR_RECORD_ID"))
