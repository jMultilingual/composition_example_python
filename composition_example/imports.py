from PySide6.QtWidgets import (QApplication, QWidget, QRadioButton, QSizePolicy, QVBoxLayout,QProxyStyle,
                               QHBoxLayout, QCommonStyle, QStyleOptionComplex, QStyleOption,
                               QLayout, QGroupBox, QPushButton, QSlider, QRadioButton, QStyleOptionButton,
                               QStyleOptionGroupBox, QStyleOptionFrame, QStyleOptionSlider, QStyleFactory,
                               QTextBrowser, QTextEdit)

from PySide6.QtGui import (QImage, QLinearGradient, QGradient, QPixmap, QPainter,
                            QPainterPath, QColor, QRadialGradient, QTextDocument,
                           QBrush, QPolygonF, QPalette, QPixmapCache,QPen,
                           QAbstractTextDocumentLayout)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QPoint, QPointF, QTimer, QMetaEnum, QRect, QSize, QFile,  QByteArray, QIODevice, QTextStream
import sys



PM_SliderLength = QCommonStyle.PM_SliderLength
PE_Frame = QCommonStyle.PE_Frame
PE_FrameFocusRect = QCommonStyle.PE_FrameFocusRect
PE_IndicatorRadioButton =  QCommonStyle.PE_IndicatorRadioButton
PE_FrameGroupBox =  QCommonStyle.PE_FrameGroupBox
PE_PanelButtonCommand =  QCommonStyle.PE_PanelButtonCommand
SE_RadioButtonClickRect =  QCommonStyle.SE_RadioButtonClickRect
SE_RadioButtonContents =  QCommonStyle.SE_RadioButtonContents
SC_SliderHandle =  QCommonStyle.SC_SliderHandle
SC_SliderGroove =  QCommonStyle.SC_SliderGroove
SC_GroupBoxContents =  QCommonStyle.SC_GroupBoxContents
SC_GroupBoxFrame =  QCommonStyle.SC_GroupBoxFrame
SC_GroupBoxLabel =  QCommonStyle.SC_GroupBoxLabel
CC_GroupBox =  QCommonStyle.CC_GroupBox
CT_RadioButton =  QCommonStyle.CT_RadioButton 
CT_PushButton =  QCommonStyle.CT_PushButton
CT_Slider =  QCommonStyle.CT_Slider
CE_RadioButtonLabel =  QCommonStyle.CE_RadioButtonLabel
CE_PushButtonLabel =  QCommonStyle.CE_PushButtonLabel
CC_ScrollBar  =  QCommonStyle.CC_ScrollBar 
CC_Slider = QCommonStyle.CC_Slider
State_Enabled = QCommonStyle.State_Enabled
State_MouseOver = QCommonStyle.State_MouseOver
State_Sunken = QCommonStyle.State_Sunken


State_On = QCommonStyle.State_On
