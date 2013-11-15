from configparser import ConfigParser
from PyQt4 import QtGui, QtCore
import os

class OkConfig(object):
    GLOBAL_DICT = {'date':['TODAY', 'YESTERDAY'], 'datetime':['CURRENT_DT'], 'time':['CURRENT_TM'], 'increment':[]}
    #date
    TODAY = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
    YESTERDAY = QtCore.QDate.currentDate().addDays(-1).toString("yyyy-MM-dd")
    
    #time
    CURRENT_TM = QtCore.QTime.currentTime().toString("hh:mm:ss")
    
    #datetime
    CURRENT_DT = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
    
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
        path =  os.environ['ONEKEY_HOME']
        self.config.read_file(open(path + "/config.conf"))
        for section in self.config.sections():
            for val in self.config.items(section):
                setattr(self, val[0].upper(), val[1])
                self.GLOBAL_DICT['increment'].append(val[0].upper())
                
    def reset(self):
        self.INCREMENT = None
        
    def save(self):
        path =  os.environ['ONEKEY_HOME']
        for section in self.config.sections():
            for val in self.config.items(section):
                self.config.set(section, val[0], self.callback(val[0].upper()))
        self.config.write(open(path + "/config.conf", "w"))
