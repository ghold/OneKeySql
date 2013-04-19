from PyQt4 import QtCore, QtGui
class SharedImage(object):
    def __init__(self):
        self.refCount = 0
        self.image = None
        self.pixmap = None
        self.matrix = QtGui.QMatrix()
        self.unscaledBoundingRect = QtCore.QRectF()
        
class OkItem(QtGui.QGraphicsItem):
    
    def __init__(self, scene=None, parent=None):
        super(OkItem, self).__init__(parent)
        
        self.opacity = 1.0
        self.locked = False
        self.prepared = False
        self.neverVisible = False
        self.noSubPixeling = False
        self.currentAnimation = None
        self.currGuide = None
        self.guideFrame = 0.0
        self.sharedImage = SharedImage()
        self.sharedImage.refCount += 1

        self.startFrame = 0.0
        self.hashKey = ''
        
    def __del__(self):
        self.sharedImage.refCount -= 1
        if self.sharedImage.refCount == 0:
            if self.hashKey:
                del OkItem.sharedImageHash[self.hashKey]
                
    def validateImage(self):
        if (self.sharedImage.matrix != OkItem.matrix ) or (self.sharedImage.image is None and self.sharedImage.pixmap is None):
            # (Re)create image according to new matrix.
            self.sharedImage.image = None
            self.sharedImage.pixmap = None
            self.sharedImage.matrix = OkItem.matrix

            # Let subclass create and draw a new image according to the new
            # matrix.
            m = OkItem.matrix
            image = self.createImage(m)
            if image is not None:
                self.sharedImage.unscaledBoundingRect = self.sharedImage.matrix.inverted()[0].mapRect(QtCore.QRectF(image.rect()))
                self.sharedImage.image = image
                return True
            else:
                return False

        return True

    def boundingRect(self):
        self.validateImage()
        return self.sharedImage.unscaledBoundingRect

    def paint(self, painter, option=None, widget=None):
        if self.validateImage():
            wasSmoothPixmapTransform = painter.testRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

            m = painter.worldMatrix()
            painter.setWorldMatrix(QtGui.QMatrix())

            x = m.dx()
            y = m.dy()
            if self.noSubPixeling:
                x = QtCore.qRound(x)
                y = QtCore.qRound(y)

            if self.sharedImage.image is not None:
                painter.drawImage(QtCore.QPointF(x, y),
                        self.sharedImage.image)
            else:
                painter.drawPixmap(QtCore.QPointF(x, y),
                        self.sharedImage.pixmap)

            if not wasSmoothPixmapTransform:
                painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform,
                        False)

    def createImage(self, matrix):
        return None

    def collidesWithItem(self, item, mode):
        return False
