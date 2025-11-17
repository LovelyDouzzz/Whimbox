from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CollapsedChatWidget(QWidget):
    """收缩状态的聊天组件"""
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.opacity_effect = None
        self.init_ui()
    
    def init_ui(self):
        self.setFixedSize(48, 48)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 允许QWidget设置背景
        self.setStyleSheet("""
            CollapsedChatWidget {
                background-color: rgba(255, 255, 255, 255);
                border-radius: 12px;
                border: 2px solid #E0E0E0;
            }
            CollapsedChatWidget:hover {
                background-color: rgba(255, 255, 255, 255);
                border: 2px solid #2196F3;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 5)
        
        icon_label = QLabel("📦")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px; border: none; background: transparent;")
        
        layout.addWidget(icon_label)
        
        # 使用 QGraphicsOpacityEffect 让整个组件（包括所有子组件）半透明
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)  # 设置透明度，0.0 完全透明，1.0 完全不透明
        self.setGraphicsEffect(self.opacity_effect)
        
        # # 启用鼠标跟踪以支持 hover 效果
        # self.setMouseTracking(True)
    
    # def enterEvent(self, event):
    #     """鼠标进入时增加不透明度"""
    #     if self.opacity_effect:
    #         self.opacity_effect.setOpacity(0.9)
    #     super().enterEvent(event)
    
    # def leaveEvent(self, event):
    #     """鼠标离开时恢复半透明"""
    #     if self.opacity_effect:
    #         self.opacity_effect.setOpacity(0.6)
    #     super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)