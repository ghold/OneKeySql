from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from OkScroll import OkScrollBar

class OkTypeBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        strList = ["固定值", "自定义标签", "标签引用"]
        self.addItems(strList)
        self.currentIndexChanged.connect(self.parent().parent().typeChanged)
        
class OkComboBoxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = OkTypeBox(parent)
        return editor
        
    def setEditorData(self, comboBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        id = comboBox.findText(value, QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(id)
        
    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class OkTagSetting(QtGui.QTableView):
    def __init__(self, tagList, parent = None):
        QtGui.QTableView.__init__(self, parent)
        self.setVerticalScrollBar(OkScrollBar())
        self.setAlternatingRowColors(True);
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        
        self.setStyleSheet("QTableView{"
                    "border: 1px solid #000;"
                    "background-color: #95a5a6;"
                    "alternate-background-color: #34495e;"
                    "selection-background-color: #323232;"
                    "gridline-color: #000;"
                    "font-size: 14px;"
                    "font-family: '微软雅黑';"
                "}"
                "QTableView::item:disabled{"
                    "background-color: #7f8c8d;"
                "}"
                "QTableView::item:disabled:alternate{"
                    "background-color: #2c3e50;"
                "}"
                "QHeaderView::section{"
                    "border-bottom: 1px solid #424242;"
                    "border-left: 1px solid #424242;"
                    "font-size: 16px;"
                    "font-family: '微软雅黑';"
                    "color: #fff;"
                    "background: #34495e;"
                "}"
                "QHeaderView {"
                    "font-size: 25px;"
                    "border: 1px solid #95a5a6;"
                    "background: #95a5a6;"
                "}"
                "QTableCornerButton::section{"
                    "border: 1px solid #424242;"
                    "background: #95a5a6;"
                "}")
        
        settingRow = len(tagList)
        #setupModel
        horizontalHeaderList = ["类型", "标签名", "默认值", "计算参数","是否可配置"]
        settingColumn = len(horizontalHeaderList)
        self.model = QtGui.QStandardItemModel(settingRow, settingColumn)
        self.model.setHorizontalHeaderLabels(horizontalHeaderList)
        
        VerticalHeaderList = []
        for row in range(settingRow):
            for column in range(settingColumn):
                index = self.model.index(row, column, QtCore.QModelIndex())
                self.model.setData(index, QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)
                #Column1
                if column == 0:
                    self.model.setData(index, "标签引用", QtCore.Qt.EditRole)
                #Colimn5 set the checkBox
                elif column == 4:
                    self.model.setData(index, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
                    self.model.itemFromIndex(index).setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
                #Column3
                elif column == 2:
                    self.model.setData(index, '不可用', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                #Column2 4
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(True)
            VerticalHeaderList.append(tagList[row][1])
        self.model.setVerticalHeaderLabels(VerticalHeaderList)    
        
        #set
        delegate = OkComboBoxDelegate()
        self.setItemDelegateForColumn(0, delegate)
        self.setModel(self.model)
        
    @pyqtSlot(int)
    def typeChanged(self, type):
        currentIndex = self.currentIndex()
        if type == 0:
            for column in range(1, 5):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 2:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                else:
                    self.model.setData(index, '不可用', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(False)
        elif type == 1:
            currentIndex = self.currentIndex()
            for column in range(1, 5):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(True)
        elif type == 2:
            currentIndex = self.currentIndex()
            for column in range(1, 5):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 4:
                    self.model.setData(index, False, QtCore.Qt.CheckStateRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif column == 2:
                    self.model.setData(index, '不可用', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.itemFromIndex(index).setEnabled(True)
