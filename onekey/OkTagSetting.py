from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from OkTagHandler import OkTagHandler
from OkScroll import OkScrollBar

class OkTypeBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        strList = ["固定值", "自定义标签", "标签引用"]
        self.addItems(strList)
        self.currentIndexChanged.connect(self.parent().parent().typeChanged)
        
class OkParamBox(QtGui.QWidget):
    closeEditor = pyqtSignal(QtGui.QWidget, QtGui.QAbstractItemDelegate.EndEditHint)
    commitData = pyqtSignal(QtGui.QWidget)
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        #OperatorComboBox
        self.operator = QtGui.QComboBox(self)
        opList = ["+", "-"]
        self.operator.addItems(opList)
        self.operator.setCurrentIndex(0)
        
        #textEdit
        self.param = QtGui.QLineEdit(self)
        self.param.setStyleSheet("QLineEdit{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 14px;"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #a8a8a8"
                "}"
                "QLineEdit:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QLineEdit:focus{"
                    "border:1px solid #7ECEFD;" 
                "}")
        self.param.editingFinished.connect(self.dataCommit)
        self.operator.activated.connect(self.param.setFocus)
        #layout
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.operator, 0)
        layout.addWidget(self.param, 1)
        self.setLayout(layout)
        
    def setValue(self, text):
        if text is not None and len(text) > 0:
            currentIndex = self.operator.findText(text[0:1])
            self.operator.setCurrentIndex(currentIndex)
            self.param.setText(text[1:])
        elif text is not None and len(text) == 0:
            self.operator.setCurrentIndex(0)
            self.param.setText('0')
        
    def getValue(self):
        return self.operator.currentText() + self.param.text()
        
    def setupToolTip(self, type):
        toolTipDict = {'datetime':'分钟', 'date':'天', 'time':'分钟', 'increment':'步长'}
        if toolTipDict.get(type, None) is not None:
           self.setToolTip('单位：' + toolTipDict[type]) 
    
    @pyqtSlot()
    def dataCommit(self):
        self.commitData.emit(self)
        self.closeEditor.emit(self, QtGui.QAbstractItemDelegate.NoHint)
        
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
    def __init__(self, tagList, varDict, confDict, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.tagList = tagList
        self.varDict = varDict
        self.confDict = confDict
        
    def createEditor(self, parent, option, index):
        row = index.row()
        self.accessList = []
        if self.varDict.get(self.tagList[row][0], None) is not None:
            self.accessList = self.varDict.get(self.tagList[row][0])
        editor = QtGui.QComboBox(parent)
        editor.addItems(self.accessList)
        editor.setEditable(True)
        return editor
        
    def setEditorData(self, comboBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        value = comboBox.findText(value, QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(value)
        
    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()
        if value != '--':
            typeIndex = model.index(index.row(), index.column()-1, QtCore.QModelIndex())
            type = model.data(typeIndex, QtCore.Qt.UserRole)
            confIndex = model.index(index.row(), index.column()+3, QtCore.QModelIndex())
            if value in self.accessList and type == 1:
                self.parent().typeChanged(2)
                model.setData(typeIndex, "标签引用", QtCore.Qt.DisplayRole)
                model.setData(typeIndex, 2, QtCore.Qt.UserRole)
            if value not in self.accessList and type == 2:
                self.parent().typeChanged(1)
                model.setData(typeIndex, "自定义标签", QtCore.Qt.DisplayRole)
                model.setData(typeIndex, 1, QtCore.Qt.UserRole)
            #set config 
            if value in self.accessList and self.confDict.get(value, None) is not None:
                model.setData(confIndex, self.confDict.get(value)[0], QtCore.Qt.CheckStateRole)
                model.setData(confIndex, self.confDict.get(value)[1], QtCore.Qt.UserRole)
            model.setData(index, value, QtCore.Qt.EditRole)
            model.setData(index, value, QtCore.Qt.UserRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class OkDefaultValDelegate(QtGui.QStyledItemDelegate):
    #if use qss for delegate, please use QStyledItemDelegate
    def __init__(self, tagList, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.tagList = tagList
        
    def createEditor(self, parent, option, index):
        row = index.row()
        editor = OkTagHandler.callback(self.tagList[row][0], None, None, parent)
        return editor
        
    def setEditorData(self, tagEdit, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        tagEdit.setValue(value)
        
    def setModelData(self, tagEdit, model, index):
        value = tagEdit.getValue()
        model.setData(index, value, QtCore.Qt.EditRole)
        model.setData(index, value, QtCore.Qt.UserRole)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class OkParamDelegate(QtGui.QStyledItemDelegate):
    #if use qss for delegate, please use QStyledItemDelegate
    def __init__(self, tagList, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.tagList = tagList
        
    def createEditor(self, parent, option, index):
        row = index.row()
        editor = OkParamBox(parent)
        editor.setupToolTip(self.tagList[row][0])
        #overload this two signal can make sure data saved and widget closed
        editor.commitData.connect(parent.parent().commitData)
        editor.closeEditor.connect(parent.parent().closeEditor)
        return editor
        
    def setEditorData(self, paramEdit, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        paramEdit.setValue(value)
        
    def setModelData(self, paramEdit, model, index):
        value = paramEdit.getValue()
        model.setData(index, value, QtCore.Qt.EditRole)
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
                    self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
                #Column3 or (Column4 and arg can't need to set)
                elif (column == 2) or (column == 3 and getattr(OkTagHandler, self.tagVars[row][0] + '_arg', None) is None):
                    self.model.setData(index, '--', QtCore.Qt.EditRole)
                    self.model.setData(index, None, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                #Column2 or (Column4 and arg can be set)
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                
            VerticalHeaderList.append(self.tagVars[row][1])
        self.model.setVerticalHeaderLabels(VerticalHeaderList)    
        
        #set Delegate for items
        delegate = OkComboBoxDelegate(self)
        self.setItemDelegateForColumn(0, delegate)
        tagNameDict = {}
        confDict = {}
        for val in self.tagLabels:
            #group type
            if tagNameDict.get(val[0], None) is None:
                tagNameDict[val[0]] = [val[1]]
            else:
                tagNameDict[val[0]].append(val[1])
            #get tags' configurable
            if val[3] is not None:
                confDict[val[1]] = (0, False)
            else:
                confDict[val[1]] = (2, True)
            
        delegate = OkTagNameDelegate(self.tagVars, tagNameDict, confDict, self)
        self.setItemDelegateForColumn(1, delegate)
        delegate = OkDefaultValDelegate(self.tagVars, self)
        self.setItemDelegateForColumn(2, delegate)
        delegate = OkParamDelegate(self.tagVars, self)
        self.setItemDelegateForColumn(3, delegate)
        self.setModel(self.model)
        
    @pyqtSlot(int)
    def typeChanged(self, type):
        currentIndex = self.currentIndex()
        if type == 0:
            for column in range(1, self.settingColumn):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 2:
                    if self.model.data(index, QtCore.Qt.EditRole) == '--':
                        self.model.setData(index, '', QtCore.Qt.EditRole)
                        self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif column == 4:
                    self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
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
                    self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif column == 3 and getattr(OkTagHandler, self.tagVars[currentIndex.row()][0] + '_arg', None) is None:
                    self.model.setData(index, '--', QtCore.Qt.EditRole)
                    self.model.setData(index, None, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                else:
                    self.model.setData(index, '', QtCore.Qt.EditRole)
                    self.model.setData(index, '', QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
        elif type == 2:
            currentIndex = self.currentIndex()
            for column in range(1, self.settingColumn):
                index = self.model.index(currentIndex.row(), column, QtCore.QModelIndex())
                if column == 4:
                    self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, False, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(True)
                elif (column == 2) or (column == 3 and getattr(OkTagHandler, self.tagVars[currentIndex.row()][0] + '_arg', None) is None):
                    self.model.setData(index, '--', QtCore.Qt.EditRole)
                    self.model.setData(index, None, QtCore.Qt.UserRole)
                    self.model.itemFromIndex(index).setEnabled(False)
                else:
                    if self.model.data(index, QtCore.Qt.EditRole) == '--':
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
        
