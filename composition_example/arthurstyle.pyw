
from imports import *
from resources import resources

def cached(img):

    pm = QPixmap()
    if QPixmapCache.find(img, pm):
        return pm

    pm = QPixmap.fromImage(QImage(img), Qt.OrderedDither| Qt.OrderedAlphaDither)
    if pm.isNull():
        return QPixmap()

    QPixmapCache.insert(img, pm)
    return pm


class ArthurStyle(QCommonStyle):

    def __init__(self, parent=None):
        super().__init__(parent)

    

    def drawHoverRect(self, painter, r):

        h = r.height()
        h2 = r.height() / float(2)
        path = QPainterPath()
        path.addRect(r.x() + h2, r.y() + 0, r.width() - h2*2, r.height())
        path.addEllipse(r.x(), r.y(), h, h)
        path.addEllipse(r.x() + r.width() - h, r.y(), h, h)
        path.setFillRule(Qt.WindingFill)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(191, 215, 191))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPath(path)

    def drawPrimitive(self, element, option, painter, widget=None):

        
    
        if element == PE_FrameFocusRect:
            pass

        elif element == PE_IndicatorRadioButton:
  
            button = option

            if button:
                hover = (button.state & State_Enabled) and (button.state & State_MouseOver)
                painter.save()
                radio = QPixmap()

                if hover:
                    self.drawHoverRect(painter, widget.rect())

                if button.state & State_Sunken:
                    radio = cached(":/images/radiobutton-on.png")
                elif button.state & State_On:
                    radio = cached(":/images/radiobutton-on.png")
                else:
                    radio = cached(":/images/radiobutton-off.png")

                painter.drawPixmap(button.rect.topLeft(), radio)

                painter.restore()

        elif element == PE_PanelButtonCommand:
          
        
            button = option
            if button:
                hover = (button.state & State_Enabled) and (button.state & State_MouseOver)
                painter.save()

                pushButton = widget

                parent = pushButton.parentWidget()

                if parent and isinstance(parent, QGroupBox):
                    lg = QLinearGradient(0, 0, 0, parent.height())
                    lg.setColorAt(0, QColor(224, 224, 224))
                    lg.setColorAt(1, QColor(255, 255, 255))
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(lg)
                    painter.setBrushOrigin(-widget.mapToParent(QPoint(0, 0)))
                    painter.drawRect(button.rect)
                    painter.setBrushOrigin(0, 0)

                down = (button.state & State_Sunken) or (button.state & State_On)

                left, right, mid = QPixmap(), QPixmap(), QPixmap()

                if down:
                    left = cached(":/images/button_pressed_cap_left.png")
                    right = cached(":/images/button_pressed_cap_right,png")
                    mid = cached(":/images/button_pressed_stretch.png")

                else:
                    left = cached(":/images/button_normal_cap_left.png")
                    right = cached(":/images/button_normal_cap_right.png")
                    mid = cached(":/images/button_normal_stretch.png")

                painter.drawPixmap(button.rect.topLeft(), left)
                painter.drawTiledPixmap(QRect(button.rect.x() + left.width(),
                                              button.rect.y(),
                                              button.rect.width() - left.width() - right.width(),
                                              left.height()),
                                        mid)
                painter.drawPixmap(button.rect.x() + button.rect.width() - right.width(),
                                   button.rect.y(),
                                   right)

                if hover:
                    painter.fillRect(widget.rect().adjusted(3, 5, -3, -5), QColor(31, 127, 31, 63))
                painter.restore()
            
        elif element == PE_FrameGroupBox:

      
            #elementが呼ばれない。なぜ？
            group = option
            

            r = group.rect

            painter.save()
            radius = 14
            radius2 = radius*2

            clipPath = QPainterPath()
            clipPath.moveTo(radius, 0)
            clipPath.arcTo(r.right() - radius2, 0, radius2, radius2, 90, -90)
            clipPath.arcTo(r.right() - radius2, r.bottom() - radius2, radius2, radius2, 0, -90)
            clipPath.arcTo(r.left(), r.bottom() - radius2, radius2, radius2, 270, -90)
            clipPath.arcTo(r.left(), r.top(), radius2, radius2, 180, -90)
            painter.setClipPath(clipPath)
            titleStretch = cached(":/images/title_stretch.png")
            topLeft = cached(":/images/groupframe_topleft.png")
            topRight = cached(":/images/groupframe_topright.png")
            bottomLeft = cached(":/images/groupframe_bottom_left.png")
            bottomRight = cached(":/images/groupframe_bottom_right.png")
            leftStretch = cached(":/images/groupframe_left_stretch.png")
            topStretch = cached(":/images/groupframe_top_stretch.png")
            rightStretch = cached(":/images/groupframe_right_stretch.png")
            bottomStretch = cached(":/images/groupframe_bottom_stretch.png")
        
            lg = QLinearGradient(0, 0, 0, r.height())
            lg.setColorAt(0, QColor(224, 224, 224))
            lg.setColorAt(1, QColor(255, 255, 255))
            painter.setPen(Qt.NoPen)
            painter.setBrush(lg)
            painter.drawRect(r.adjusted(0, titleStretch.height()/2, 0, 0))
            painter.setClipping(False)

            topFrameOffset = titleStretch.height()/2 - 2
            painter.drawPixmap(r.topLeft() + QPoint(0, topFrameOffset), topLeft)
            painter.drawPixmap(r.topRight()- QPoint(topRight.width() - 1, 0) + QPoint(0, topFrameOffset), topRight)
            painter.drawPixmap(r.bottomLeft() - QPoint(0, bottomLeft.height() -1), bottomLeft)
            painter.drawPixmap(r.bottomRight() - QPoint(bottomRight.width() - 1, bottomRight.height() - 1), bottomRight)

            left = r
            left.setY(r.y() + topLeft.height() + topFrameOffset)
            left.setWidth(leftStretch.width())
            left.setHeight(r.height() - topLeft.height() - bottomLeft.height() - topFrameOffset)
            painter.drawTiledPixmap(left, leftStretch)

            top = r
            top.setX(r.x() + topLeft.width())
            top.setY(r.y() + topFrameOffset)
            top.setWidth(r.width() - topLeft.width() - topRight.width())
            top.setHeight(topLeft.height())
            painter.drawTiledPixmap(top, topStretch)

            right = r
            right.setX(r.right() - rightStretch.width() + 1)
            right.setY(r.y() + topRight.height() + topFrameOffset)
            right.setWidth(rightStretch.width())
            right.setHeight(r.height() - topRight.height() - bottomRight.height() - topFrameOffset)

            painter.drawTiledPixmap(right, rightStretch)

            bottom = r
            bottom.setX(r.x() + bottomLeft.width())
            bottom.setY(r.bottom() - bottomStretch.height()+1)
            bottom.setWidth(r.width() - bottomLeft.width() - bottomRight.width())
            bottom.setHeight(bottomLeft.height())
            painter.drawTiledPixmap(bottom, bottomStretch)
            painter.restore()

        else:
            return QCommonStyle.drawPrimitive(self, element, option, painter, widget)
            
            
            

    def drawControl(self, element, option, painter, widget):
        
        if element == CE_RadioButtonLabel:
           
            button = option

            if not button.text:
                QCommonStyle.drawControl(self, element, option, painter, widget)

            else:
                painter.save()
                painter.setPen(Qt.black)
                painter.drawText(button.rect, Qt.AlignVCenter, button.text)
                painter.restore()

        elif element == CE_PushButtonLabel:

        
            button = option

            if not button.text:
                QCommonStyle.drawControl(self, element, option, painter, widget)

            else:
                painter.save()
                painter.setPen(Qt.black)
                painter.drawText(button.rect, Qt.AlignVCenter | Qt.AlignHCenter, button.text)
                painter.restore()

        else:
            return QCommonStyle.drawControl(self, element, option, painter, widget)
            

    def drawComplexControl(self, control, option, painter, widget):
        
        if control == CC_ScrollBar:

       
        
            slider = option
            groove = self.subControlRect(CC_Slider, option, SC_SliderGroove, widget)
            handle = self.subControlRect(CC_Slider, option, SC_SliderHandle, widget)

            painter.save()

            hover = (slider.state & State_Enabled) and (slider.state & State_MouseOver)
            if hover:
                moderated = widget.rect().adjusted(0, 4, 0, -4)
                self.drawHoverRect(painter, moderated)

            if (option.subControls & SC_SliderGroove) and groove.isValid():
                grv = cached(":/images/slider_bar.png")
                painter.drawPixmap(QRect(groove.x() + 5, groove.y(),
                                         groove.width() - 10, grv.height()),
                                   grv)
            if (option.subControls & SC_SliderHandle) and handle.isValid():
                hndl = cached(":/images/slider_thumb_on.png")
                painter.drawPixmap(handle.topLeft(), hndl)

            painter.restore()

        elif control == CC_GroupBox:        
        
            if isinstance(option, QStyleOptionGroupBox):
                
                groupBox = option
                groupBoxCopy = option
                #本当はこうしたかった。groupBoxCopy.subControls &= ~SC_GroupBoxLabel
                groupBoxCopy.subControls &= ~SC_GroupBoxLabel
                QCommonStyle.drawComplexControl(self, control, groupBoxCopy, painter, widget)

                if (groupBox.subControls & SC_GroupBoxLabel):
                    r = groupBox.rect
                    titleLeft = cached(":/images/title_cap_left.png")
                    titleRight = cached(":/images/title_cap_right.png")
                    titleStretch = cached(":/images/title_stretch.png")
                    txt_width = groupBox.fontMetrics.horizontalAdvance(groupBox.text) + 20
                    painter.drawPixmap(r.center().x() - txt_width/2, 0, titleLeft)
                    tileRect = self.subControlRect(control, groupBox, SC_GroupBoxLabel, widget)
                    painter.drawTiledPixmap(tileRect, titleStretch)
                    painter.drawPixmap(tileRect.x() + tileRect.width() , 0, titleRight)
                    opacity = 31
                    painter.setPen(QColor(0, 0, 0, opacity))
                    painter.drawText(tileRect.translated(0, 1), Qt.AlignVCenter | Qt.AlignHCenter, option.text)
                    painter.drawText(tileRect.translated(2, 1), Qt.AlignVCenter | Qt.AlignHCenter, option.text)
                    painter.setPen(QColor(0, 0, 0, opacity*2))
                    painter.drawText(tileRect.translated(1, 1),
                                     Qt.AlignVCenter | Qt.AlignHCenter, option.text)
                    painter.setPen(Qt.white)
                    painter.drawText(tileRect, Qt.AlignVCenter|Qt.AlignHCenter, option.text)

                else:
                    QCommonStyle.drawComplexControl(self, control, option, painter, widget)

                    
            else:
                QCommonStyle.drawComplexControl(self, control, option, painter, widget)

        else:
            QCommonStyle.drawComplexControl(self, control, option, painter, widget)
            
                

    def sizeFromContents(self, type,  option, size, widget):

        newSize = QCommonStyle.sizeFromContents(self, type, option, size, widget)

        if type == CT_RadioButton:
            newSize += QSize(20, 0)

        elif type == CT_PushButton:
            newSize.setHeight(26)

        elif type == CT_Slider:
            newSize.setHeight(27)

        return newSize

    def subControlRect(self, cc, opt, sc, widget):

       
        rect = QCommonStyle.subControlRect(self, cc, opt, sc, widget)
        if cc == CC_GroupBox:

            group = opt
            if group:
                rect =  QCommonStyle.subControlRect(self, cc, opt, sc, widget)
                if cc == SC_GroupBoxContents:
                    rect =  QCommonStyle.subControlRect(self, cc, opt, sc, widget)
                    rect.adjust(0, -8, 0, 0)

                elif cc == SC_GroupBoxFrame:
                    rect = group.rect

                elif cc == SC_GroupBoxLabel:
                    titleLeft = cached(":/images/title_cap_left.png")
                    titleRight = cached(":/images/title_cap_right.png")
                    titleStretch = cached(":/images/title_stretch.png")
                    txt_width = group.fontMetrics.horizontalAdvance(group.text) + 20
                    rect = QRect(group.rect.center().x() - txt_width/2 + titleLeft.width(), 0,
                                 txt_width - titleLeft.width() - titleRight.width(),
                                 titleStretch.height())
                    
        if cc == CC_Slider and sc == SC_SliderHandle:
            rect.setWidth(13)
            rect.setHeight(27)

        elif cc == CC_Slider and sc == SC_SliderGroove:
            rect.setHeight(9)
            rect.moveTop(27/2 - 9/2)

        return rect
    
            
    def subElementRect(self, element, option, widget):

        if element == SE_RadioButtonClickRect:
            r = widget.rect()

        elif element == SE_RadioButtonContents:

            r = widget.rect().adjusted(20, 0, 0, 0)

        else:
            r = QCommonStyle.subElementRect(self, element, option, widget)

        if isinstance(widget, QRadioButton):
            r = r.adjusted(5, 0, -5, 0)

        return r
                

    def pixelMetric(self, metric, option, widget):

        if metric == PM_SliderLength:
            return 13

        return QCommonStyle.pixelMetric(self, metric, option, widget)

    def polish(self, widget):

        if isinstance(widget, QPalette):
            widget.setColor(QPalette.Window, QColor(241, 241, 241))

        else:
    
            
            if widget.layout() and isinstance(widget, QGroupBox):
                if not widget.findChild(QGroupBox):
                    widget.layout().setSpacing(0)
                    widget.layout().setContentsMargins(12, 12, 12, 12)
                else:
                    widget.layout().setContentsMargins(13, 13, 13, 13)

            if isinstance(widget, (QPushButton, QRadioButton, QSlider)):
                widget.setAttribute(Qt.WA_Hover)

            pal = widget.palette()
            if widget.isWindow():
                pal.setColor(QPalette.Window, QColor(241, 241, 241))
                widget.setPalette(pal)
            

    def unppolish(self, widget):

        if isinstance(widget, (QPushButton, QRadioButton, QSlider)):
            widget.setAttribute(Qt.WA_Hover, False)
    
