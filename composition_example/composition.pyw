from PySide6.QtWidgets import QApplication, QGroupBox, QPushButton, QSlider,  QWidget, QRadioButton, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from PySide6.QtGui import  QPainter, QImage, QTextDocument, QColor, QLinearGradient, QPen
from PySide6.QtCore import Qt, QEvent, QTimer, QPointF, Slot, QDateTime, QLineF, QPoint, QRectF, QSize, QSizeF

from PySide6.QtOpenGL import QOpenGLTextureBlitter

import sys

animationInterval = 15

NoObject = 0
Circle = 1
Rectangle = 2
Image = 3

from resources import resources
from arthurstyle import ArthurStyle
from arthurwidgets import ArthurFrame

def rectangle_around(p, size=QSize(250, 200)):
    
    rect = QRectF(p, size)
    rect.translate(-size.width()/2, -size.height()/2)
    return rect

class CompositionWidget(QWidget):

    class ObjectType:
        NoObject = 0
        Circle = 1
        Rectangle = 2
        Image = 3
        

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

        

        self.viewLayout = QHBoxLayout(self)
        self.viewLayout.addWidget(self.view)
        self.viewLayout.addWidget(self.mainGroup)

        self.mainGroupLayout = QVBoxLayout(self.mainGroup)
        self.mainGroupLayout.addWidget(self.circleColorGroup)
        self.mainGroupLayout.addWidget(self.circleAlphaGroup)
        self.mainGroupLayout.addWidget(self.modesGroup)
        self.mainGroupLayout.addStretch()
        self.mainGroupLayout.addWidget(self.animateButton)
        self.mainGroupLayout.addWidget(self.whatsThisButton)
        self.mainGroupLayout.addWidget(self.showSourceButton)

        self.mainGroupLayout.addWidget(self.enableOpenGLButton)

        self.modesLayout = QGridLayout(self.modesGroup)
        self.modesLayout.addWidget(self.rbClear, 0, 0)
        self.modesLayout.addWidget(self.rbSource, 1, 0)
        self.modesLayout.addWidget(self.rbDest, 2, 0)
        self.modesLayout.addWidget(self.rbSourceOver, 3, 0)
        self.modesLayout.addWidget(self.rbDestOver, 4, 0)
        self.modesLayout.addWidget(self.rbSourceIn, 5, 0)
        self.modesLayout.addWidget(self.rbDestIn, 6, 0)
        self.modesLayout.addWidget(self.rbSourceOut, 7, 0)
        self.modesLayout.addWidget(self.rbDestOut, 8, 0)
        self.modesLayout.addWidget(self.rbSourceATop, 9, 0)
        self.modesLayout.addWidget(self.rbDestATop, 10, 0)
        self.modesLayout.addWidget(self.rbXor, 11, 0)

        self.modesLayout.addWidget(self.rbPlus, 0, 1)
        self.modesLayout.addWidget(self.rbMultiply, 1, 1)
        self.modesLayout.addWidget(self.rbScreen, 2, 1)
        self.modesLayout.addWidget(self.rbOverlay, 3, 1)
        self.modesLayout.addWidget(self.rbDarken, 4, 1)
        self.modesLayout.addWidget(self.rbLighten, 5, 1)
        self.modesLayout.addWidget(self.rbColorDodge, 6, 1)
        self.modesLayout.addWidget(self.rbColorBurn, 7, 1)
        self.modesLayout.addWidget(self.rbHardLight, 8, 1)
        self.modesLayout.addWidget(self.rbSoftLight, 9, 1)
        self.modesLayout.addWidget(self.rbDifference, 10, 1)
        self.modesLayout.addWidget(self.rbExclusion, 11, 1)

        self.circleColorLayout = QVBoxLayout(self.circleColorGroup)
        self.circleColorLayout.addWidget(self.circleColorSlider)
        self.circleAlphaLayout = QVBoxLayout(self.circleAlphaGroup)
        self.circleAlphaLayout.addWidget(self.circleAlphaSlider)

        self.view.loadDescription(":html/composition.html")
        self.view.loadSourceFile(":cpp/composition.cpp")


        self.rbSourceOut.animateClick()
        self.setWindowTitle(self.tr("Composition Modes"))
        
       

    def initUI(self):

        self.view = CompositionRenderer(self)

        self.mainGroup = QGroupBox(title="Composition Modes", parent=self)

        self.modesGroup = QGroupBox(title="Mode", parent=self)

        self.circleColorGroup = QGroupBox(title = "Circle color", parent=self.mainGroup)
        self.circleColorSlider = QSlider(Qt.Horizontal, minimum=0, maximum=350, parent=self.circleColorGroup)
        self.circleColorSlider.valueChanged.connect(self.view.setCircleColor)
        self.circleColorSlider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        self.circleAlphaGroup = QGroupBox(title="Circle alpha", parent=self.mainGroup)
        self.circleAlphaSlider = QSlider(Qt.Horizontal, minimum=0, maximum=255, parent=self.circleAlphaGroup)
        
        self.circleAlphaSlider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.circleAlphaSlider.valueChanged.connect(self.view.setCircleAlpha)

        self.showSourceButton = QPushButton(text=self.tr("Show Source"), parent=self.mainGroup, clicked=self.view.showSource)

        self.enableOpenGLButton = QPushButton(text="Use OpenGL", checkable=True, checked=self.view.usesOpenGL(), parent=self.mainGroup)
        

        self.whatsThisButton = QPushButton(text="What's This?", checkable=True, parent=self.mainGroup )
        self.whatsThisButton.clicked[bool].connect(self.view.setDescriptionEnabled)

        self.animateButton = QPushButton(text="Animated", checkable=True, checked=True, parent=self.mainGroup)
        self.animateButton.clicked[bool].connect(self.view.setAnimationEnabled)
        self.m_cycle_enabled = False

        self.rbClear = QRadioButton(text= self.tr("Clear"), parent=self.modesGroup, clicked=self.view.setClearMode)
        self.rbSource = QRadioButton(text=self.tr("Source"), parent=self.modesGroup, clicked=self.view.setSourceMode)
        self.rbDest = QRadioButton(text=self.tr("Destination"), parent=self.modesGroup, clicked=self.view.setDestMode)
        self.rbSourceOver = QRadioButton(text=self.tr("Source Over"), parent=self.modesGroup, clicked=self.view.setSourceOverMode)
        self.rbDestOver = QRadioButton(text=self.tr("Destination Over"), parent=self.modesGroup, clicked=self.view.setDestOverMode)
        self.rbSourceIn = QRadioButton(text=self.tr("Source In"), parent=self.modesGroup, clicked=self.view.setSourceInMode)
        self.rbDestIn = QRadioButton(text=self.tr("Dest In"), parent=self.modesGroup, clicked=self.view.setDestInMode)
        self.rbSourceOut = QRadioButton(text=self.tr("Source Out"), parent=self.modesGroup, clicked=self.view.setSourceOutMode)
        self.rbDestOut = QRadioButton(text=self.tr("Dest Out"), parent=self.modesGroup,clicked=self.view.setDestOutMode)
        self.rbSourceATop = QRadioButton(text=self.tr("Source Atop"), parent=self.modesGroup, clicked=self.view.setSourceAtopMode)
        self.rbDestATop = QRadioButton(text=self.tr("Dest Atop"), parent=self.modesGroup, clicked=self.view.setDestAtopMode)
        self.rbXor = QRadioButton(text=self.tr("Xor"), parent=self.modesGroup, clicked=self.view.setXorMode)

        self.rbPlus = QRadioButton(text=self.tr("Plus"), parent=self.modesGroup, clicked=self.view.setPlusMode)
        self.rbMultiply = QRadioButton(text=self.tr("Multiply"), parent=self.modesGroup, clicked=self.view.setMultiplyMode)
        self.rbScreen = QRadioButton(text=self.tr("Screen"), parent=self.modesGroup, clicked=self.view.setScreenMode)
        self.rbOverlay = QRadioButton(text=self.tr("Overlay"), parent=self.modesGroup, clicked=self.view.setOverlayMode)
        self.rbDarken = QRadioButton(text=self.tr("Darken"), parent=self.modesGroup, clicked=self.view.setDarkenMode)
        self.rbLighten = QRadioButton(text=self.tr("Lighten"), parent=self.modesGroup, clicked=self.view.setLightenMode)
        self.rbColorDodge = QRadioButton(text=self.tr("Color Dodge"), parent=self.modesGroup, clicked=self.view.setColorDodgeMode)
        self.rbColorBurn = QRadioButton(text=self.tr("Color Burn"), parent=self.modesGroup, clicked=self.view.setColorBurnMode)
        self.rbHardLight = QRadioButton(text=self.tr("Hard Light"), parent=self.modesGroup, clicked=self.view.setHardLightMode)
        self.rbSoftLight = QRadioButton(text=self.tr("Soft Light"), parent=self.modesGroup, clicked=self.view.setSoftLightMode)
        self.rbDifference = QRadioButton(text=self.tr("Difference"), parent=self.modesGroup, clicked=self.view.setDifferenceMode)
        self.rbExclusion = QRadioButton(text=self.tr("Exclusion"), parent=self.modesGroup, clicked=self.view.setExclusionMode)
        

        
    def nextMode(self):
        pass

class CompositionRenderer(ArthurFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_circle_pos = QPoint(200, 100)
        self.m_animation_enabled = True
        self.m_animationTimer = self.startTimer(animationInterval)

        self.m_image = QImage(":/images/flower.jpg")
        self.m_image.setAlphaChannel(QImage(":/images/flower_alpha.jpg"))
        self.m_circle_alpha = 127
        self.m_circle_hue = 255
        self.m_current_object = NoObject
        self.m_composition_mode = QPainter.CompositionMode_SourceOut

        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.m_pbuffer_size = 1024
        
    
        self.m_buffer = QImage()
        self.m_base_buffer = QImage()

  
        self.m_offset = QPoint()

        self.m_current_object = NoObject


        self.m_fbo = None
   
        self.m_base_tex= 0
        self.m_compositing_tex = 0
        self.m_previous_size = QSize()
        self.m_blitter = QOpenGLTextureBlitter()


    def paint(self, painter):

        
        if self.m_buffer.size() != self.size():

            self.m_buffer = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
            self.m_base_buffer = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)

            self.m_base_buffer.fill(0)

            p = QPainter(self.m_base_buffer)

            self.drawBase(p)
     
        self.m_buffer = QImage(self.m_base_buffer)
    
        p = QPainter(self.m_buffer)
        self.drawSource(p)
        
        painter.drawImage(0, 0, self.m_buffer)
        
        

    def setCirclePos(self, pos):

        oldRect = rectangle_around(self.m_circle_pos).toAlignedRect()
        self.m_circle_pos = pos
        newRect = rectangle_around(self.m_circle_pos).toAlignedRect()

        self.update(oldRect|newRect)
        

    def sizeHint(self):

        return QSize(500, 400)

    def animationEnabled(self):

        return self.m_animation_enabled

    def circleColor(self):

        return self.m_circle_hue

    def circleAlpha(self):

        return self.m_circle_alpha

    def mousePressEvent(self, event):

        self.setDescriptionEnabled(False)

        circle = rectangle_around(self.m_circle_pos)

        if circle.contains(event.position()):
            self.m_current_object = Circle
            self.m_offset = circle.center().toPoint() - event.position().toPoint()

        elif self.m_animation_enabled:
                self.killTimer(self.m_animationTimer)
                self.m_animationTimer = 0
        

    def mouseMoveEvent(self, event):

        if self.m_current_object == Circle:
            self.setCirclePos(event.position().toPoint() + self.m_offset)

    def mouseReleaseEvent(self, event):

        self.m_current_object = NoObject

        if self.m_animation_enabled:
            self.m_animationTimer = self.startTimer(animationInterval)


    def timerEvent(self, event):

        if event.timerId() == self.m_animationTimer:
            self.updateCirclePos()

    @Slot()
    def setClearMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Clear
        self.update()

    @Slot()
    def setSourceMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Source
        self.update()

    @Slot()
    def setDestMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Destination
        self.update()

    @Slot()
    def setSourceOverMode(self):

        self.m_composition_mode = QPainter.CompositionMode_SourceOver
        self.update()

    @Slot()
    def setDestOverMode(self):

        self.m_composition_mode = QPainter.CompositionMode_DestinationOver
        self.update()

    @Slot()
    def setSourceInMode(self):

        self.m_composition_mode = QPainter.CompositionMode_SourceIn
        self.update()

    @Slot()
    def setDestInMode(self):

        self.m_composition_mode = QPainter.CompositionMode_DestinationIn
        self.update()

    @Slot()
    def setSourceOutMode(self):

        self.m_composition_mode = QPainter.CompositionMode_SourceOut
        self.update()

    @Slot()
    def setDestOutMode(self):

        self.m_composition_mode = QPainter.CompositionMode_DestinationOut
        self.update()

    @Slot()
    def setSourceAtopMode(self):

        self.m_composition_mode = QPainter.CompositionMode_SourceAtop
        self.update()

    @Slot()
    def setDestAtopMode(self):

        self.m_composition_mode = QPainter.CompositionMode_DestinationAtop
        self.update()

    @Slot()
    def setXorMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Xor
        self.update()

    @Slot()
    def setPlusMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Plus
        self.update()

    @Slot()
    def setMultiplyMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Multiply
        self.update()

    @Slot()
    def setScreenMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Screen
        self.update()

    @Slot()
    def setOverlayMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Overlay
        self.update()

    @Slot()
    def setDarkenMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Darken
        self.update()

    @Slot()
    def setLightenMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Lighten
        self.update()

    @Slot()
    def setColorDodgeMode(self):

        self.m_composition_mode = QPainter.CompositionMode_ColorDodge
        self.update()

    @Slot()
    def setColorBurnMode(self):

        self.m_composition_mode = QPainter.CompositionMode_ColorBurn
        self.update()

    @Slot()
    def setHardLightMode(self):

        self.m_composition_mode = QPainter.CompositionMode_HardLight
        self.update()

    @Slot()
    def setSoftLightMode(self):

        self.m_composition_mode = QPainter.CompositionMode_SoftLight
        self.update()

    @Slot()
    def setDifferenceMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Difference
        self.update()

    @Slot()
    def setExclusionMode(self):

        self.m_composition_mode = QPainter.CompositionMode_Exclusion
        self.update()

    @Slot()
    def setCircleAlpha(self, alpha):

        self.m_circle_alpha = alpha
        self.update()

    @Slot()
    def setCircleColor(self, hue):

        self.m_circle_hue = hue
        self.update()

    @Slot()
    def setAnimationEnabled(self, enabled):

        if self.m_animation_enabled == enabled:
            return

        self.m_animation_enabled = enabled
        if enabled:
            self.m_animationTimer = self.startTimer(animationInterval)
        else:
            self.killTimer(self.m_animationTimer)
            self.m_animationTimer = 0

    def updateCirclePos(self):

   
        import math
        if self.m_current_object != NoObject:
            return

        dt = QDateTime.currentDateTime()

        t = dt.toMSecsSinceEpoch() / 1000.0

        x = self.width() / 2 + (math.cos(t*8/11) + math.sin(-t))*self.width() / 4
        y = self.height() / 2 + math.sin(t*6/7) + math.cos(t*1.5)*self.height()/4

        self.setCirclePos(QLineF(self.m_circle_pos, QPointF(x, y)).pointAt(0.02))
      

    def drawBase(self, p):
     
      
        p.setPen(Qt.NoPen)

        rect_gradient = QLinearGradient(0, 0, 0, self.height())
        rect_gradient.setColorAt(0, Qt.red)
        rect_gradient.setColorAt(0.17, Qt.yellow)
        rect_gradient.setColorAt(0.33, Qt.green)
        rect_gradient.setColorAt(0.50, Qt.cyan)
        rect_gradient.setColorAt(0.66, Qt.blue)
        rect_gradient.setColorAt(0.81, Qt.magenta)
        rect_gradient.setColorAt(1, Qt.red)

        p.setBrush(rect_gradient)
        p.drawRect(self.width() / 2, 0, self.width() / 2, self.height())

        alpha_gradient = QLinearGradient(0, 0, self.width(), 0)
        alpha_gradient.setColorAt(0, Qt.white)
        alpha_gradient.setColorAt(0.2, Qt.white)
        alpha_gradient.setColorAt(0.5, Qt.transparent)
        alpha_gradient.setColorAt(0.8, Qt.white)
        alpha_gradient.setColorAt(1, Qt.white)

        
        p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        
        p.setBrush(alpha_gradient)
        p.drawRect(0, 0, self.width(), self.height())
        
        p.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        p.setPen(Qt.NoPen)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawImage(self.rect(), self.m_image)
    

        

    def drawSource(self, p):

        
        p.setPen(Qt.NoPen)
        p.setRenderHint(QPainter.Antialiasing)

        p.setCompositionMode(self.m_composition_mode)

        circle_rect = rectangle_around(self.m_circle_pos)
        color = QColor.fromHsvF(self.m_circle_hue/ 360.0, 1, 1, self.m_circle_alpha / 255.0)
        circle_gradient = QLinearGradient(circle_rect.topLeft(), circle_rect.bottomRight())
        
        circle_gradient.setColorAt(0, color.lighter())
        circle_gradient.setColorAt(0.5, color)
        circle_gradient.setColorAt(1, color.darker())
        p.setBrush(circle_gradient)
        p.drawEllipse(circle_rect)
        
 
def main():

    app = (
           QApplication()
           if QApplication.instance() is None
           else
           QApplication.instance()
           )

    arthurStyle = ArthurStyle()
    compWidget = CompositionWidget()
    compWidget.setStyle(arthurStyle)

    #
    widgets = compWidget.findChildren(QWidget)
    for w in widgets:
        w.setStyle(arthurStyle)

    compWidget.show()

    return sys.exit(app.exec())

if __name__ == "__main__":
    main()
