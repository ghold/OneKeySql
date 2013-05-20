from PyQt4 import QtGui, QtCore, Qt

class OkMainToolBar(QtGui.QToolBar):
    
    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self, parent)
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.addWidget(spacer)
        self.addWidget(MinButton())
        self.maxOrResizeButton = MaxOrResizeButton()
        self.addWidget(self.maxOrResizeButton)
        self.addWidget(closeButton())
        
    def setGeometryByHeight(self,  height):
        if self.parent() is not None:
            self.setGeometry(0,  0,  self.parent().rect().width(),  height)
            
    def mousePressEvent(self,event):
       if event.button() == QtCore.Qt.LeftButton:
           self.parent().dragPosition = event.globalPos() - self.parent().frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.parent().isMaximized():
            self.parent().move(event.globalPos() - self.parent().dragPosition)
            event.accept() 
    
    def mouseDoubleClickEvent(self,  event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.parent().isMaximized():
                self.parent().showNormal()
                self.maxOrResizeButton.updateStyle()
                if self.parent().editWidget is not None:
                    self.parent().editWidget.update()
                self.update()
                event.accept()
            else:
                self.parent().showMaximized()
                self.maxOrResizeButton.updateStyle()
                if self.parent().editWidget is not None:
                    self.parent().editWidget.update()
                self.update()
                event.accept()
                
    def paintEvent(self,  event):
        self.setGeometryByHeight(44)
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        #tmpBrush = QtGui.QBrush(QtGui.QColor(110,  202,  199))
        #tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()

class OkEditToolBar(QtGui.QToolBar):
    
    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self, parent)
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.addWidget(backButton())
        self.addWidget(spacer)
        self.addWidget(MinButton())
        self.maxOrResizeButton = MaxOrResizeButton()
        self.addWidget(self.maxOrResizeButton)
        self.addWidget(closeButton())
            
    def setGeometryByHeight(self,  height):
        if self.parent() is not None:
            self.setGeometry(0,  0,  self.parent().rect().width(),  height)
            
    def mousePressEvent(self,event):
       if event.button() == QtCore.Qt.LeftButton:
           self.topLevelWidget().dragPosition = event.globalPos() - self.topLevelWidget().frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.topLevelWidget().isMaximized():
            self.topLevelWidget().move(event.globalPos() - self.topLevelWidget().dragPosition)
            event.accept() 
    
    def mouseDoubleClickEvent(self,  event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.topLevelWidget().isMaximized():
                self.topLevelWidget().showNormal()
                self.maxOrResizeButton.updateStyle()
                if self.topLevelWidget().editWidget is not None:
                    self.topLevelWidget().editWidget.update()
                self.update()
                self.topLevelWidget().update()
                event.accept()
            else:
                self.topLevelWidget().showMaximized()
                self.maxOrResizeButton.updateStyle()
                if self.topLevelWidget().editWidget is not None:
                    self.topLevelWidget().editWidget.update()
                self.update()
                self.topLevelWidget().update()
                event.accept()
                
    def paintEvent(self,  event):
        self.setGeometryByHeight(44)
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(50,  50,  50))
        tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()

class windowButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setMaximumSize(26, 26)
        self.setFlat(1)
                
class closeButton(windowButton):
    def __init__(self, parent=None):
        windowButton.__init__(self, parent)
        self.setStyleSheet("windowButton{"
                    "height: 24px;"
                    "width: 24px;"
                    "background: url(:/images/xmark_24x24_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/xmark_24x24_white.png)"
                "}")
        
    def mousePressEvent(self, event):
        self.topLevelWidget().dragPosition = event.globalPos() - self.topLevelWidget().frameGeometry().topLeft()
        self.topLevelWidget().exit()
        event.accept()
        
class MaxOrResizeButton(windowButton):
    def __init__(self, parent=None):
        windowButton.__init__(self, parent)
        self.updateStyle()
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.topLevelWidget().dragPosition = event.globalPos() - self.topLevelWidget().frameGeometry().topLeft()
            if self.topLevelWidget().isMaximized():
                self.topLevelWidget().showNormal()
                self.updateStyle()
                if self.topLevelWidget().editWidget is not None:
                    self.topLevelWidget().editWidget.update()
                self.parent().update()
                self.topLevelWidget().update()
                event.accept()
            else:
                self.topLevelWidget().showMaximized()
                self.updateStyle()
                if self.topLevelWidget().editWidget is not None:
                    self.topLevelWidget().editWidget.update()
                self.parent().update()
                self.topLevelWidget().update()
                event.accept()
                
    def updateStyle(self):
        if self.topLevelWidget().isMaximized():
            self.setStyleSheet("windowButton{"
                    "height: 24px;"
                    "width: 24px;"
                    "background: url(:/images/resize_24x24_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/resize_24x24_white.png)"
                "}")
        else:
            self.setStyleSheet("windowButton{"
                    "height: 24px;"
                    "width: 24px;"
                    "background: url(:/images/max_24x24_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/max_24x24_white.png)"
                "}")

class MinButton(windowButton):
    def __init__(self, parent=None):
        windowButton.__init__(self, parent)
        self.setStyleSheet("windowButton{"
                    "height: 24px;"
                    "width: 24px;"
                    "background: url(:/images/min_24x24_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/min_24x24_white.png)"
                "}")
        
    def mousePressEvent(self, event):
        self.topLevelWidget().dragPosition = event.globalPos() - self.topLevelWidget().frameGeometry().topLeft()
        self.topLevelWidget().showMinimized()
        event.accept()
        
class backButton(windowButton):
    def __init__(self, parent=None):
        windowButton.__init__(self, parent)
        self.setMaximumSize(42, 40)
        self.setStyleSheet("windowButton{"
                    "height: 40px;"
                    "width: 38px;"
                    "background: url(:/images/back_40x38_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/back_40x38_white.png)"
                "}")
        
    def mousePressEvent(self, event):
        self.topLevelWidget().dragPosition = event.globalPos() - self.topLevelWidget().frameGeometry().topLeft()
        self.parent().parent().close()
        event.accept()
