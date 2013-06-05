from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from OkScroll import OkScrollBar

class OkTypeBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        strList = ["固定值", "自定义标签", "标签引用"]
        self.addItems(strList)
        self.currentIndexChanged.connect(self.parent().parent().typeChanged)
        
class OkComboBoxDelegate(QtGui.QStyledItemDelegate):
    #if use qss for delegate, please use QStyledItemDelegate
    def __init__(self, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        editor = OkTypeBox(parent)
        return editor
        
    def setEditorData(self, comboBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        value = comboBox.findText(value, QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(value)
        
    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)
        value = comboBox.findText(value, QtCore.Qt.MatchExactly)
        model.setData(index, value, QtCore.Qt.UserRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class OkTagNameDelegate(QtGui.QStyledItemDelegate):
    #if use qss for delegate, please use QStyledItemDelegate
    def __init__(self, tagList, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.tagList = tagList
        
    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        editor.addItems(self.tagList)
        editor.setEditable(True)
        return editor
        
    def setEditorData(self, comboBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        value = comboBox.findText(value, QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(value)
        
    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)
        value = comboBox.findText(value, QtCore.Qt.MatchExactly)
        model.setData(index, value, QtCore.Qt.UserRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class OkTagSetting(QtGui.QTableView):
    def __init__(self, tagVars, tagLabels, data, parent = None):
        QtGui.QTableView.__init__(self, parent)
        self.tagVars = tagVars
        self.tagLabels = tagLabels
        self.data = data
        self.setVerticalScrollBar(OkScrollBar())
        self.setAlternatingRowColors(False)
        self.setShowGrid(False)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        
        self.setStyleSheet("QTableView{"
                    "border: 1px solid #323232;"
                    "background-color: #323232;"
                    "font-size: 14px;"
                    "font-family: '微软雅黑';"
                    "color: #FFF"
                "}"
                "QTableView::item{"
                    "border-left: 1px solid #A6A6A6;"
                    "border-bottom: 1px solid #A6A6A6;"
                "}"
                "QTableView::item:hover{"
                    "background-color:rgba(205, 92, 92, 100)"
                "}"
                "QTableView::item:selected{"
                    "background-color:rgba(205, 92, 92, 100)"
                "}"
                "QTableView::item:disabled{"
                    "color: #474747;"
                    "background-color: #2B2B2B;"
                "}"
                "QHeaderView::section{"
                    "border-top: 1px solid #323232;"
                    "border-left: 1px solid #323232;"
                    "border-right: 1px solid #A6A6A6;"
                    "border-bottom: 1px solid #A6A6A6;"
                    "font-size: 16px;"
                    "font-family: '微软雅黑';"
                    "color: #B5B5B5;"
                    "background: #323232;"
                "}"
                "QHeaderView::section:vertical{"
                    "border-right: 0px solid #323232;"
                "}"
                "QHeaderView::section:horizontal{"
                    "border-left: 1px solid #A6A6A6;"
                    "border-right: 0px solid #323232;"
                "}"
                "QHeaderView::section:hover{"
                    "border: 1px solid #1c98cc;"
                "}"
                "QHeaderView {"
                    "font-size: 25px;"
                    "background: #323232;"
                "}"
                "QTableCornerButton::section{"
                    "border-top: 1px solid #323232;"
                    "border-left: 1px solid #323232;"
                    "border-right: 0px solid #ccc;"
                    "border-bottom: 1px solid #ccc;"
                    "background: #323232;"
                "}")
        
        self.settingRow = len(self.tagVars)
        #setupModel
        horizontalHeaderList = ["类型", "标签名", "默认值", "计算参数","是否可配置"]
        self.settingColumn = len(horizontalHeaderList)
        self.model = QtGui.QStandardItemModel(self.settingRow, self.settingColumn)
        self.model.setHorizontalHeaderLabels(horizontalHeaderList)
        self.setSelectionMode(3)
        self.setSelectionBehavior(1)
        
        VerticalHeaderList = []
        for row in range(self.settingRow):
            for column in range(self.settingColumn):
                index = self.model.index(row, column, QtCore.QModelIndex())
                self.model.setData(index, QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)
                #Column1
                if column == 0:
                    self.model.setData(index, "标签引用", QtCore.Qt.EditRole)
                    self.model.setData(index, 2, QtCore.Qt.UserRole)
                #Colimn5 set the checkBox
                elif column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
                #Column3
                elif column == 2:
                    self.model.setData(index, '--', QtCore.Qt.EditRole)
                    self.model.setData(index, None, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                #Column2 4
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
            VerticalHeaderList.append(self.tagVars[row][1])
        self.model.setVerticalHeaderLabels(VerticalHeaderList)    
        
        #set Delegate for items
        delegate = OkComboBoxDelegate(self)
        self.setItemDelegateForColumn(0, delegate)
        tagNameList = []
        for val in self.tagLabels:
            print(val)
        #delegate = OkTagNameDelegate(tagNameList, self)
        #self.setItemDelegateForColumn(1, delegate)
        self.setModel(self.model)
        
    @pyqtSlot(int)
    def typeChanged(self, type):
        currentIndex = self.currentIndex()
        if type == 0:
            for column in range(1, self.settingColumn):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 2:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                else:
                    self.model.setData(index, '--', QtCore.Qt.EditRole)
                    self.model.setData(index, None, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
        elif type == 1:
            currentIndex = self.currentIndex()
            for column in range(1, self.settingColumn):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
        elif type == 2:
            currentIndex = self.currentIndex()
            for column in range(1, self.settingColumn):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif column == 2:
                    self.model.setData(index, '--', QtCore.Qt.EditRole)
                    self.model.setData(index, None, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
    
    def setupModelDict(self):
        modelDict = {}
        modelDict['data_id'] = self.data['id']
        modelDict['from'] = 'testunit'
        modelDict['type'] = 'testunit'
        modelDict['tags'] = {}
        for row in range(self.settingRow):
            tag = self.model.headerData(row, QtCore.Qt.Vertical)
            modelDict['tags'][tag] = []
            for column in range(self.settingColumn):
                index = self.model.index(row, column, QtCore.QModelIndex())
                if self.model.data(index) == '' and column == 1:
                    self.edit(index)
                    return None
                modelDict['tags'][tag].append(self.model.data(index, QtCore.Qt.UserRole))
            modelDict['tags'][tag].append(self.tagVars[row][0])
        return modelDict
