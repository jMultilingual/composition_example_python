
from imports import *

class ArthurFrame(QWidget):

    descriptionEnabledChanged = Signal(bool)

    def __init__(self, parent=None, flags = Qt.WindowFlags()):

        super().__init__(parent, flags)

        self.m_sourceFileName = ""

        self.m_tile = QPixmap(128, 128)
        pt = QPainter(self.m_tile)
        color = QColor(230, 230, 230)
        pt.fillRect(0, 0, 64, 64, color)
        pt.fillRect(64, 64, 64, 64, color)
        pt.end()


        
        self.m_stops = []
       

        self.m_spread = QGradient.PadSpread
        self.m_gradientType = Qt.LinearGradientPattern

        self.m_glWindow = None
        self.m_glWidget = None
        self.m_use_opengl = False
        
        self.m_showDoc = False
        self.m_preferImage = False
   
   

        self.m_foreground = False
        self.m_background = True
        self.m_sorround = False


        



    
    def paintEvent(self, event):


        self.static_image = None

        painter = QPainter()

        if self.preferImage() and not self.m_use_opengl:
            if not self.static_image or self.static_image.size() != self.size():
                self.static_image = QImage(self.size(), QImage.Format_RGB32)

            painter.begin(self.static_image)

            o = 10

            bg = self.palette().brush(QPalette.Window)
            painter.fillRect(0, 0, o, o, bg)
            painter.fillRect(self.width() - o, 0, o, o, bg)
            painter.fillRect(0, self.height() - o, o, o, bg)
            painter.fillRect(self.width() - o, self.height() - o, o, o, bg)

        else:
            if self.m_use_opengl and self.m_glWindow.isValid():
                self.m_glWindow.makeCurrent()

                painter.begin(self.m_glWindow)
                painter.fillRect(QRectF(0, 0, self.m_glWindow.width(), self.m_glWindow.height(), self.palette().color(self.backgroundRole())))
            else:
                painter.begin(self)


        painter.setClipRect(event.rect())
        painter.setRenderHint(QPainter.Antialiasing)

        clipPath = QPainterPath()

        r = self.rect()
        left = r.x() + 1
        top = r.y() + 1
        right = r.right()
        bottom = r.bottom()
        radius2 = 8 * 2

        clipPath.moveTo(right - radius2, top)
        clipPath.arcTo(right - radius2, top, radius2, radius2, 90, -90)
        clipPath.arcTo(right - radius2, bottom - radius2, radius2, radius2, 0, -90)
        clipPath.arcTo(left, bottom - radius2, radius2, radius2, 270, -90)
        clipPath.arcTo(left, top, radius2, radius2, 180, -90)
        clipPath.closeSubpath()
        
        painter.save()
        painter.setClipPath(clipPath, Qt.IntersectClip)

        painter.drawTiledPixmap(self.rect(), self.m_tile)
        
                                 

        self.paint(painter)

        painter.restore()

        painter.save()
        
        if self.m_showDoc:
            self.paintDescription(painter)

        painter.restore()

        level = 180
        painter.setPen(QPen(QColor(level, level, level), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(clipPath)

        if self.preferImage() and not self.m_use_opengl:

            painter.end()
            painter.begin(self)
            painter.drawImage(event.rect(), self.static_image, event.rect())
            
        if self.m_use_opengl:
            self.m_glWindow.update()

        

        
    def paintDescription(self, painter):

        if not self.m_document:
            return

        pageWidth = max(self.width() - 100, 100)
        pageHeight = max(self.height() - 100,100)

        if pageWidth != self.m_document.pageSize().width():
            self.m_document.setPageSize(QSize(pageWidth, pageHeight))

        textRect = QRect(self.width() / 2 - pageWidth/2,
                         self.height() /2 - pageHeight/2,
                         pageWidth,
                         pageHeight)

        pad = 10

        clearRect = textRect.adjusted(-pad, -pad, pad, pad)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 63))

        shade = 10
        painter.drawRect(clearRect.x() + clearRect.width() + 1,
                         clearRect.y() + shade,
                         shade,
                         clearRect.height() + 1)
        painter.drawRect(clearRect.x() + shade,
                         clearRect.y() + clearRect.height() + 1,
                         clearRect.width() - shade + 1,
                         shade)
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setBrush(QColor(255, 255, 255, 220))
        painter.setPen(Qt.black)
        painter.drawRect(clearRect)

        painter.setClipRegion(textRect, Qt.IntersectClip)
        painter.translate(textRect.topLeft())

        g = QLinearGradient(0, 0, 0, textRect.height())
        g.setColorAt(0, Qt.black)
        g.setColorAt(0.9, Qt.black)
        g.setColorAt(1, Qt.transparent)

        pal = self.palette()
        pal.setBrush(QPalette.Text, g)

        ctx = QAbstractTextDocumentLayout.PaintContext()
        ctx.palette = pal
        ctx.clip = QRect(0, 0, textRect.width(), textRect.height())
        self.m_document.documentLayout().draw(painter, ctx)

    def loadSourceFile(self, sourceFile):

        self.m_sourceFileName = sourceFile

    def showSource(self):

        if self.findChild(QTextBrowser):
            return

        contents = ""

        if not self.m_sourceFileName:
            contents = self.tr(f"No source for widget: {self.objectName()}")

        else:
            f = QFile(self.m_sourceFileName)
            if not f.open(QFile.ReadOnly):
                contents = self.tr(f"Could not open file: {self.m_sourceFileName}")
      
            else:
          
                contents = f.readAll()
                out = QTextStream(contents)
                contents = out.readAll()
               
                
        contents = contents.replace("&", "&amp")
        contents = contents.replace("<", "&lt")
        contents = contents.replace(">", "&gt")

        keywords= [
                   "for ", "if ", "switch ", " int ",
                   "#include ", "const", "void ", "uint ",
                   "case ", "double ", "#define ", "static",
                   "new", "this"
                   ]

        for keyword in keywords:
            contents = contents.replace(keyword, "<font color=olive>" + keyword + "</font>")
        contents = contents.replace("(int ", "(<font color=olive><b>int </b></font>")

        ppKeywords = ["#ifdef", "#ifndef", "#if", "#endif", "#else"]


        for keyword in ppKeywords:
            contents = contents.replace("(\\d\\d?)", "<font color=navy>\\1</font>")

        contents = contents.replace("(//.+?)\\n", "<font color=red>\\1</font>\n")
        contents = contents.replace("(\".+?\")", "<font color=green>\\1</font>")

        html = "<html><pre>" + contents + "</pre></html>"

        self.sourceViewer = QTextBrowser()
        self.sourceViewer.setWindowTitle(self.tr("Source: {}".format(self.m_sourceFileName[:-5])))
        self.sourceViewer.setParent(self, Qt.Dialog)
        self.sourceViewer.setAttribute(Qt.WA_DeleteOnClose)
        self.sourceViewer.setLineWrapMode(QTextEdit.NoWrap)
        self.sourceViewer.setHtml(html)
        self.sourceViewer.resize(600, 600)
        self.sourceViewer.show()
        

    def setDescriptionEnabled(self, enabled):

        if self.m_showDoc != enabled:
            self.m_showDoc = enabled
            self.descriptionEnabledChanged.emit(self.m_showDoc)
            self.update()

    def setDescription(self, text):

        self.m_document = QTextDocument(self)

        if isinstance(text, QByteArray):

            out = QTextStream(text, QIODevice.ReadOnly)
            text = out.readAll()
        self.m_document.setHtml(text)
        

    def preferImage(self):

        return self.m_preferImage

    def setPreferImage(self, pi):

        self.m_preferImage = pi

    def resizeEvent(self, e):

        if self.m_glWidget:
            self.m_glWidget.setGeometry(0, 0, e.size().width(), e.size().height())

        QWidget.resizeEvent(self, e)

    def loadDescription(self, fileName):

        textFile = QFile(fileName)
        text = ""

        if not textFile.open(QFile.ReadOnly):
            text = f"Unable to load resource file: {fileName}"
        else:
            text = textFile.readAll()
       

        self.setDescription(text)
        

    def paint(self, painter):
        
        pts = self.m_hoverPoints.points()

        g = QGradient()

        if self.m_gradientType == Qt.LinearGradientPattern:
            g = QLinearGradient(pts.at(0), pts.at(1))
           

        elif self.m_gradientType == Qt.RadialGradientPattern:
            g = QRadialGradient(pts.at(0), min(self.width(), self.height()) / 3.0, pts.at(1))

        else:
            l = QLineF(pts.at(0), pts.at(1))
            angle = QLineF(0, 0, 1, 0).angleTo(l)
            g = QConicalGradient(pts.at(0), angle)
        
        for stop in self.m_stops:
            g.setColorAt(stop[0], stop[1])

        g.setSpread(self.m_spread)

        if self.m_background:

            painter.setBrush(g)
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())

        elif self.m_sorround:
            

            pen = painter.pen()
            pen.setStyle(Qt.SolidLine)
            pen.setWidth(200)
            pen.setBrush(g)
            brush = painter.brush()
            brush.setStyle(Qt.NoBrush)
        
            painter.setPen(pen)
            painter.setBrush(brush)

            painter.drawRect(self.rect())

        elif self.m_foreground:

            
            pen = painter.pen()            
            pen.setBrush(g)
            painter.setPen(pen)
           
        
            painter.setFont(self.font())
            
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        

    def sizeHint(self):

        return QSize(400, 400)

    def hoverPoints(self):

        return self.m_hoverPoints

    def mousePressEvent(self, e):

        self.setDescriptionEnabled(False)
        
     
        return super().mousePressEvent(e)

    def setGradientStops(self, stops):

        self.m_stops = stops
        self.update()

    def setPadSpread(self):
        
        self.m_spread = QGradient.PadSpread
        self.update()

    def setRepeatSpread(self):

        self.m_spread = QGradient.RepeatSpread
        self.update()

    def setReflectSpread(self):

        self.m_spread = QGradient.ReflectSpread
        self.update()

    def setLinearGradient(self):

        self.m_gradientType = Qt.LinearGradientPattern
        self.update()

    def setRadialGradient(self):

        self.m_gradientType = Qt.RadialGradientPattern
        self.update()

    def setConicalGradient(self):

        self.m_gradientType = Qt.ConicalGradientPattern
        self.update()

    def createGlWindow(self):

        self.m_glWindow = QOpenGLWindow()
        f = QSurfaceFormat.defaultFormat()
        f.setSamples(4)
        f.setAlphaBufferSize(8)
        f.setStencilBufferSize(8)
        self.m_glWindow.setFormat(f)
        self.m_glWindow.setFlags(Qt.WindowTransparentForInput)
        self.m_glWindow.resize(self.width(), self.height())
        self.m_glWidget = QWidget.createWindowContainer(self.m_glWindow, self)
        self.m_glWindow.create()
        
    def enableOpenGL(self, use_opengl):

        if self.m_use_opengl == use_opengl:
            return

        self.m_use_opengl = use_opengl

        if not self.m_glWindow and use_opengl:
            self.createGlWindow()
            QApplication.postEvent(self, QResizeEvent(self.size(), self.size()))

        if use_opengl:
            self.m_glWidget.show()

        else:
            if self.m_glWidget:
                self.m_glWidget.hide()

        self.update()
        

    def usesOpenGL(self):

        return self.m_use_opengl

