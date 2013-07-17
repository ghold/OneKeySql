from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from OkTagHandler import OkTagHandler
from OkScroll import OkScrollBar
from OkConfig import OkConfig

class OkTypeBox(QtGui.QComboBox):
    changeType = pyqtSignal(int, QtCore.QModelIndex)
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        strList = ["固定值", "自定义标签", "标签引用"]
        self.addItems(strList)
        self.currentIndexChanged.connect(self.typeChanged)
        self.changeType.connect(self.parent().parent().typeChanged)
        
    @pyqtSlot(int)
    def typeChanged(self, type):
        self.changeType.emit(type, self.parent().parent().currentIndex())
        
class OkDefaultValBox(QtGui.QWidget):
    closeEditor = pyqtSignal(QtGui.QWidget, QtGui.QAbstractItemDelegate.EndEditHint)
    commitData = pyqtSignal(QtGui.QWidget)
    def __init__(self, subtype, config, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.subtype = subtype
        self.config = config
        self.defGlobalVal = None
        self.defCustomVal = None
        self.subeditor = None
        
        self.comboBox = QtGui.QComboBox()
        strList = ["","全局变量", "固定值"]
        self.comboBox.addItems(strList)
        self.comboBox.setCurrentIndex(0)
        self.comboBox.activated.connect(self.typeActivated)
        
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)
        
    def setValue(self, text):
        if text is not None and len(text) > 0:
            if self.config.GLOBAL_DICT.get(self.subtype, None) is not None and text in self.config.GLOBAL_DICT[self.subtype]:
                self.defGlobalVal = text
                self.comboBox.setItemText(0, text)
            else:
                self.customVal = text
                self.comboBox.setItemText(0,text)
        
    def getValue(self):
        if self.defGlobalVal is not None:
            return self.defGlobalVal
        elif self.defCustomVal is not None:
            return self.defCustomVal
        return self.comboBox.itemText(0)
        
    @pyqtSlot(int)
    def typeActivated(self, type):
        if type == 1:
            self.defCustomVal = None
            self.subeditor = QtGui.QComboBox()
            self.subeditor.setStyleSheet("QComboBox{"
                    "border:1px solid #000000;"
                    "height: 25px;"
                    "font-size: 14px;"
                "}")
            if self.config.GLOBAL_DICT.get(self.subtype, None) is not None:
                self.subeditor.addItems(self.config.GLOBAL_DICT[self.subtype])
                self.subeditor.activated.connect(self.dataCommit)
                if self.defGlobalVal is not None:
                    idx = self.subeditor.findText(self.defGlobalVal)
                    self.subeditor.setCurrentIndex(idx)
                else:
                    self.subeditor.setCurrentIndex(-1)
        elif type == 2:
            self.defGlobalVal = None
            self.subeditor = OkTagHandler.callback(self.subtype, None, None, None)
            self.subeditor.editingFinished.connect(self.dataCommit)
            if self.defCustomVal is not None:
                self.subeditor.setValue(self.defCustomVal)
        else:
            self.dataCommit()
            return
        self.layout().addWidget(self.subeditor)
        self.subeditor.setFocus(True)
        self.layout().removeWidget(self.comboBox)
        
    @pyqtSlot()
    @pyqtSlot(int)
    def dataCommit(self):
        if self.subeditor is not None:
            try:
                self.defCustomVal = self.subeditor.getValue()
            except AttributeError:
                self.defGlobalVal = self.subeditor.currentText()
        self.commitData.emit(self)
        self.closeEditor.emit(self, QtGui.QAbstractItemDelegate.NoHint)
        
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
    def __init__(self, tagList, varDict, confDict, customTagsUser, tagConn, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.tagList = tagList
        self.varDict = varDict
        self.confDict = confDict
        self.customTags = {}
        self.customTagsOwner = {}
        self.customTagsUser = customTagsUser
        self.tagConn = tagConn
        
    def createEditor(self, parent, option, index):
        row = index.row()
        self.accessList = []
        self.customList = []
        if self.varDict.get(self.tagList[row][0], None) is not None:
            self.accessList = self.varDict.get(self.tagList[row][0])
        if self.customTags.get(self.tagList[row][0], None) is not None:
            self.customList = self.customTags.get(self.tagList[row][0])
            self.finalList = self.accessList + self.customList
        else:
            self.finalList = self.accessList.copy()
        #delete the editing one
        
        editor = QtGui.QComboBox(parent)
        editor.addItems(self.finalList)
        editor.setEditable(True)
        return editor
        
    def setEditorData(self, comboBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        comboBox.setEditText("%s"%value)
        
    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()
        if value != '--':
            typeIndex = model.index(index.row(), index.column()-1, QtCore.QModelIndex())
            type = model.data(typeIndex, QtCore.Qt.UserRole)
            confIndex = model.index(index.row(), index.column()+3, QtCore.QModelIndex())
            
            #init
            for key, val in self.tagConn.items():
                removeList = [index.row()]
                if type == 1 and self.customTagsOwner.get(index.row(), None) is not None and self.customTagsUser.get(key, None) is not None and self.customTagsOwner[index.row()] != value:
                    removeList = [index.row()] + self.customTagsUser[key]
                for i in removeList:
                    if val is not None and i in val:
                        val.remove(i)
                    break
            
            currentRowTag = self.customTagsOwner.get(index.row(), None)
            currentRowTagList = self.customTags.get(self.tagList[index.row()][0], None)
            # accessList use
            if value in self.accessList and type == 1:
                if currentRowTag is not None and len(currentRowTagList) >0:
                    #init custom tags user
                    tag = "%s-%s"%(self.tagList[index.row()][0], self.customTagsOwner[index.row()])
                    if self.customTagsUser.get(tag, None) is not None:
                        for val in self.customTagsUser[tag]:
                            userIndex = model.index(val, 0, QtCore.QModelIndex())
                            self.parent().typeChanged(2, userIndex)
                            model.setData(userIndex, "标签引用", QtCore.Qt.DisplayRole)
                            model.setData(userIndex, 2, QtCore.Qt.UserRole)
                    currentRowTagList.remove(currentRowTag)
                self.parent().typeChanged(2)
                model.setData(typeIndex, "标签引用", QtCore.Qt.DisplayRole)
                model.setData(typeIndex, 2, QtCore.Qt.UserRole)
            
            if value not in self.finalList and len(value)>0:
                #customTags
                currentRowTag = self.customTagsOwner.get(index.row(), None)
                currentRowTagList = self.customTags.get(self.tagList[index.row()][0], None)
                if currentRowTagList is not None:
                    if currentRowTag is not None and len(currentRowTagList)>0:
                        #init custom tags user
                        tag = "%s-%s"%(self.tagList[index.row()][0], self.customTagsOwner[index.row()])
                        if self.customTagsUser.get(tag, None) is not None:
                            for val in self.customTagsUser[tag]:
                                userIndex = model.index(val, 0, QtCore.QModelIndex())
                                self.parent().typeChanged(2, userIndex)
                                model.setData(userIndex, "标签引用", QtCore.Qt.DisplayRole)
                                model.setData(userIndex, 2, QtCore.Qt.UserRole)
                        #
                        self.customTags.get(self.tagList[index.row()][0]).remove(self.customTagsOwner[index.row()])
                    self.customTags[self.tagList[index.row()][0]].append(value)
                else:
                    self.customTags[self.tagList[index.row()][0]] = [value]
                
                #add custom tag owner
                self.customTagsOwner[index.row()] = value
                if type == 2 :
                    self.parent().typeChanged(1)
                    model.setData(typeIndex, "自定义标签", QtCore.Qt.DisplayRole)
                    model.setData(typeIndex, 1, QtCore.Qt.UserRole)
                    
            if len(value)==0 and self.customTagsOwner.get(index.row(), None) is not None:
                #init custom tags user
                tag = "%s-%s"%(self.tagList[index.row()][0], self.customTagsOwner[index.row()])
                if self.customTagsUser.get(tag, None) is not None:
                    for val in self.customTagsUser[tag]:
                        userIndex = model.index(val, 0, QtCore.QModelIndex())
                        self.parent().typeChanged(2, userIndex)
                        model.setData(userIndex, "标签引用", QtCore.Qt.DisplayRole)
                        model.setData(userIndex, 2, QtCore.Qt.UserRole)
                self.customTags.get(self.tagList[index.row()][0]).remove(self.customTagsOwner[index.row()] )
                self.customTagsOwner.pop(index.row())
                
            #customList use
            if value not in self.finalList and self.customTagsOwner.get(index.row(), None) is not None:
                self.customTagsOwner[index.row()] = value
            if value in self.customList:
                if self.customTagsOwner.get(index.row(), None) is None:
                    self.parent().typeChanged(2)
                    model.setData(typeIndex, "标签引用", QtCore.Qt.DisplayRole)
                    model.setData(typeIndex, 2, QtCore.Qt.UserRole)
                elif self.customTagsOwner[index.row()] != value and len(self.customTagsOwner[index.row()])>0 and self.customTagsOwner[index.row()] in self.customTags.get(self.tagList[index.row()][0]):
                    self.customTags.get(self.tagList[index.row()][0]).remove(self.customTagsOwner[index.row()])
                    self.parent().typeChanged(2)
                    model.setData(typeIndex, "标签引用", QtCore.Qt.DisplayRole)
                    model.setData(typeIndex, 2, QtCore.Qt.UserRole)
            
            #set tagConn
            if len(value) > 0:
                tag = "%s-%s"%(self.tagList[index.row()][0], value)
                if self.tagConn.get(tag, None) is not None:
                    self.tagConn[tag].append(index.row())
                else:
                    self.tagConn[tag]=[index.row()]
            
            #customUser
            for key, val in self.customTagsUser.items():
                if val is not None and index.row() in val:
                    val.remove(index.row())
                    break
                    
            if value in self.customList:
                if (self.customTagsOwner.get(index.row(), None) is not None  and self.customTagsOwner[index.row()] != value) or self.customTagsOwner.get(index.row(), None) is None:
                    tag = "%s-%s"%(self.tagList[index.row()][0], value)
                    if self.customTagsUser.get(tag, None) is not None:
                        self.customTagsUser[tag].append(index.row())
                    else:
                        self.customTagsUser[tag]=[index.row()]
                    
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
    def __init__(self, tagList, config, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.tagList = tagList
        self.config = config
        
    def createEditor(self, parent, option, index):
        row = index.row()
#        subeditor = OkTagHandler.callback(self.tagList[row][0], None, None, parent)
        editor = OkDefaultValBox(self.tagList[row][0], self.config, parent)
        
        #overload this two signal can make sure data saved and widget closed
        editor.commitData.connect(parent.parent().commitData)
        editor.closeEditor.connect(parent.parent().closeEditor)
        return editor
        
    def setEditorData(self, defValEdit, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        defValEdit.setValue(value)
        
    def setModelData(self, defValEdit, model, index):
        value = defValEdit.getValue()
        model.setData(index, value, QtCore.Qt.EditRole)
        model.setData(index, value, QtCore.Qt.UserRole)
        
    def updateEditorGeometry(self, defValEdit, option, index):
        defValEdit.setGeometry(option.rect)
        
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
        self.customTagsUser = {}
        self.tagConn = {}
        self.config = OkConfig()
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
        self.model.itemChanged.connect(self.checkableChange)
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
            
        delegate = OkTagNameDelegate(self.tagVars, tagNameDict, confDict, self.customTagsUser, self.tagConn, self)
        self.setItemDelegateForColumn(1, delegate)
        delegate = OkDefaultValDelegate(self.tagVars, self.config, self)
        self.setItemDelegateForColumn(2, delegate)
        delegate = OkParamDelegate(self.tagVars, self)
        self.setItemDelegateForColumn(3, delegate)
        self.setModel(self.model)
        
    @pyqtSlot(int, QtCore.QModelIndex)
    def typeChanged(self, type, ind=None):
        currentIndex = self.currentIndex()
        needRemove = [currentIndex.row()]
        if ind is not None:
            currentIndex = ind
            tpIndex = self.model.index(currentIndex.row(), 1, QtCore.QModelIndex())
            value = self.model.data(tpIndex, QtCore.Qt.EditRole)
            tag = "%s-%s"%(self.tagVars[currentIndex.row()][0], value)
            if self.customTagsUser.get(tag, None) is not None:
                needRemove = [currentIndex.row()] + self.customTagsUser[tag]
                self.customTagsUser.pop(tag)
            if self.tagConn.get(tag, None) is not None: 
                for row in needRemove:
                    if row in self.tagConn[tag]:
                        self.tagConn[tag].remove(row)
        
        for row in needRemove:
            if type == 0:
                for column in range(1, self.settingColumn):
                    index = self.model.index(row, column, QtCore.QModelIndex())
                    if column == 2:
                        if self.model.data(index, QtCore.Qt.EditRole) == '--':
                            self.model.setData(index, '', QtCore.Qt.EditRole)
                            self.model.setData(index, '', QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(True)
                    elif column == 4:
                        self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
                        self.model.setData(index, None, QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(False)
                    else:
                        self.model.setData(index, '--', QtCore.Qt.EditRole)
                        self.model.setData(index, None, QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(False)
            elif type == 1:
                for column in range(1, self.settingColumn):
                    index = self.model.index(row, column, QtCore.QModelIndex())
                    if column == 4:
                        self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
                        self.model.setData(index, None, QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(True)
                    elif column == 3 and getattr(OkTagHandler, self.tagVars[currentIndex.row()][0] + '_arg', None) is None:
                        self.model.setData(index, '--', QtCore.Qt.EditRole)
                        self.model.setData(index, None, QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(False)
                    else:
                        if self.model.data(index, QtCore.Qt.EditRole) == '--' or ind is not None:
                            self.model.setData(index, '', QtCore.Qt.EditRole)
                            self.model.setData(index, '', QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(True)
                type += 1
                continue
            elif type == 2:
                for column in range(1, self.settingColumn):
                    index = self.model.index(row, column, QtCore.QModelIndex())
                    if column == 4:
                        self.model.setData(index, 0, QtCore.Qt.CheckStateRole)
                        self.model.itemFromIndex(index).setEnabled(True)
                    elif (column == 2) or (column == 3 and getattr(OkTagHandler, self.tagVars[currentIndex.row()][0] + '_arg', None) is None):
                        self.model.setData(index, '--', QtCore.Qt.EditRole)
                        self.model.setData(index, None, QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(False)
                    else:
                        if self.model.data(index, QtCore.Qt.EditRole) == '--' or ind is not None:
                            self.model.setData(index, '', QtCore.Qt.EditRole)
                            self.model.setData(index, '', QtCore.Qt.UserRole)
                        self.model.itemFromIndex(index).setEnabled(True)
    
    @pyqtSlot(QtGui.QStandardItem)
    def checkableChange(self, item):
        if item.column() != 4:
            return
        chData = item.data(QtCore.Qt.CheckStateRole)
        userData = item.data(QtCore.Qt.UserRole)
        for key , val in self.tagConn.items():
            if val is not None and item.row() in val:
                for row in val:
                    index = self.model.index(int(row), 4, QtCore.QModelIndex())
                    if self.model.data(index, QtCore.Qt.CheckStateRole) == chData and self.model.data(index, QtCore.Qt.UserRole) == userData:
                        continue
                    self.model.setData(index, chData, QtCore.Qt.CheckStateRole)
                    self.model.setData(index, userData, QtCore.Qt.UserRole)
    
    def setupModelDict(self):
        modelDict = {}
        modelDict['data_id'] = self.data['id']
        try:
            int(id)
            modelDict['from'] = 'testunit'
        except TypeError:
            modelDict['from'] = 'spec'
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
                if column == 4:
                    tagState = self.model.data(index, QtCore.Qt.UserRole)
                    varState = self.model.data(index, QtCore.Qt.CheckStateRole) 
                    if tagState is not None:
                        if varState == 2 and not tagState:
                            modelDict['tags'][tag].append(1)
                        elif varState == 0 and tagState:
                            modelDict['tags'][tag].append(2)
                        else:
                            modelDict['tags'][tag].append(0)
                    else:
                        if varState == 2 :
                            modelDict['tags'][tag].append(True)
                        else:
                            modelDict['tags'][tag].append(False)
                else:
                    modelDict['tags'][tag].append(self.model.data(index, QtCore.Qt.UserRole))
            modelDict['tags'][tag].append(self.tagVars[row][0])
        return modelDict
        
