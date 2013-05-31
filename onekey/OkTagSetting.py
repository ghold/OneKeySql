from PyQt4 import QtGui, QtCore

class OkComboBoxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        strList = ["固定值", "自定义标签", "标签引用"]
        editor.addItems(strList)
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

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    model = QtGui.QStandardItemModel(4, 2)
    tableView = QtGui.QTableView()
    tableView.setModel(model)

    delegate = OkComboBoxDelegate()
    tableView.setItemDelegate(delegate)

    for row in range(4):
        for column in range(2):
            index = model.index(row, column, QtCore.QModelIndex())
            model.setData(index, "固定值")

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec_())
