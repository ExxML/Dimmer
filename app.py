import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QApplication
from PyQt6.QtGui import QFont

class App(QWidget):
    opacity_changed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Window setup
        self.setWindowTitle('Dimmer')
        self.setFixedSize(280, 120)
        
        # Set window flags to stay on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Title bar with close button
        title_bar = QHBoxLayout()
        title_label = QLabel('Dimmer')
        title_label.setFont(QFont('Microsoft JhengHei', 13, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #ffb634;')
        
        # Close button setup
        self.close_btn = QPushButton('×', self)
        self.close_btn.setFixedSize(35, 30)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #ffb634;
                border: none;
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 3px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #ffb634;
                color: #242424;
                border-radius: 0px;
            }
        ''')
        
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        
        # Opacity control section
        opacity_layout = QVBoxLayout()
        opacity_layout.setSpacing(5)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.on_opacity_changed)
        
        self.slider.setStyleSheet('''
            QSlider::groove:horizontal {
                background: #1a1a1a;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ffb634;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #ffc44d;
            }
            QSlider::sub-page:horizontal {
                background: #ffb634;
                border-radius: 4px;
            }
        ''')
        
        # Value label below slider
        self.value_label = QLabel('50%')
        self.value_label.setFont(QFont('Microsoft JhengHei', 9))
        self.value_label.setStyleSheet('''
            color: #ffffff;
            background-color: #3a3a3a;
            border-radius: 6px;
            padding: 4px 8px;
        ''')
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Container to align label to the right
        value_container = QHBoxLayout()
        value_container.addStretch()
        value_container.addWidget(self.value_label)
        
        opacity_layout.addWidget(self.slider)
        opacity_layout.addLayout(value_container)
        
        # Add all to main layout
        main_layout.addLayout(title_bar)
        main_layout.addLayout(opacity_layout)
        
        self.setLayout(main_layout)
        
        # Apply overall styling
        self.setStyleSheet('''
            QWidget {
                background-color: #242424;
                border-radius: 10px;
            }
        ''')
        
        # Position close button at top-right corner
        self.close_btn.move(self.width() - self.close_btn.width(), 0)
        
        # Position in bottom right corner
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width()
        y = screen.height() - self.height()
        self.move(x, y)
        
    def on_opacity_changed(self, value):
        self.value_label.setText(f'{value}%')
        self.opacity_changed.emit(value * 0.8 / 100) # Cap at 80% opacity
