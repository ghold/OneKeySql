from PyQt4 import  Qt

class OkModuleButton(Qt.QPushButton):
    def __init__(self,  text, image, parent=None):
        Qt.QPushButton.__init__(self, text, parent)
        self.setMinimumSize(200, 35)
        self.image = image
        self.setFlat(1)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        
        self.setStyleSheet("QPushButton{"
                    "border: 0px;"
                    "color: #2e2e2e;"
                    "padding-left: 36px;"
                    "font-size: 18px;"
                    "font-family: '微软雅黑';"
                    "background: #fff url("+self.image+") no-repeat"
                "}"
                "QPushButton:checked{"
                    "color: #fff;"
                    "border: 0px;"
                    "padding-left: 36px;"
                    "background: #2185c5 url("+self.image+") no-repeat"
                "}"
                "QPushButton:hover{"
                    "color: #fff;"
                    "border: 0px;"
                    "padding-left: 36px;"
                    "background: #4da6ea url("+self.image+") no-repeat"
                "}")
        
class OkExecButton(Qt.QPushButton):
    def __init__(self,  text, parent=None):
        Qt.QPushButton.__init__(self, text, parent)
        
        self.setStyleSheet("QPushButton{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 16px;"
                    "font-family: '微软雅黑';"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #FFF;"
                "}"
                "QPushButton:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QPushButton:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        
class windowButton(Qt.QPushButton):
    def __init__(self, parent=None):
        Qt.QPushButton.__init__(self, parent)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setMaximumSize(26, 26)
        self.setFlat(1)
    
class OkAddCaseButton(windowButton):
    def __init__(self, parent=None):
        windowButton.__init__(self, parent)
        self.setStyleSheet("windowButton{"
                    "height: 24px;"
                    "width: 24px;"
                    "background: url(:/images/plus_24x24_gray.png)"
                "}"
                "windowButton:hover {"
                    "background: url(:/images/plus_24x24_blue.png)"
                "}")
                
class OkCancelButton(windowButton):
    def __init__(self, parent=None):
        windowButton.__init__(self, parent)
        self.setStyleSheet("windowButton{"
                    "height: 24px;"
                    "width: 24px;"
                    "background: url(:/images/xmark_24x24_gray.png)"
                "}"
                "windowButton:hover {"
                    "background: url(:/images/xmark_24x24_red.png)"
                "}")
