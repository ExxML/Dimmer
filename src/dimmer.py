from overlay import Overlay
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QAction, QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QApplication, QSystemTrayIcon, QMenu
import os
import sys
import json

class TickBar(QWidget):
    def __init__(self, slider, parent = None):
        super().__init__(parent)
        self.slider = slider
        self.setFixedHeight(10)

    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()

        minor_pen = QPen(QColor("#8a8a8a"))
        minor_pen.setWidth(1)
        major_pen = QPen(QColor("#ffb634"))
        major_pen.setWidth(1)

        # Draw 11 ticks from 0% to 100% inclusive
        for i in range(11):
            # Add padding to ensure first and last ticks are visible
            x = 5 + round(i * (w - 10) / 10)
            if i % 5 == 0:  # Major ticks at 0%, 50%, 100%
                painter.setPen(major_pen)
                length = 7
            else:  # Minor ticks at 10%, 20%, 30%, 40%, 60%, 70%, 80%, 90%
                painter.setPen(minor_pen)
                length = 5
            painter.drawLine(x, h - length, x, h - 1)
        painter.end()

class App(QWidget):
    opacity_changed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Window setup
        self.setWindowTitle('Dimmer')
        self.setFixedSize(280, 140)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Translucent bg for rounded corners

        # Set window flags to stay on top
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
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
        
        # Minimize button setup
        self.min_btn = QPushButton('–', self)
        self.min_btn.setFixedSize(35, 30)
        self.min_btn.clicked.connect(self.hide)
        self.min_btn.setStyleSheet('''
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
        
        # Close button setup
        self.close_btn = QPushButton('×', self)
        self.close_btn.setFixedSize(35, 30)
        self.close_btn.clicked.connect(self.quit_app)
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
                border-top-right-radius: 8px;
            }
        ''')
        
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        
        # Opacity control section
        opacity_layout = QVBoxLayout()
        opacity_layout.setSpacing(5)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setFixedHeight(20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(self.load_opacity())
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
        
        # Opacity label below slider
        self.opacity_label = QLabel(f"{self.slider.value()}%")
        self.opacity_label.setFont(QFont('Microsoft JhengHei', 10))
        self.opacity_label.setStyleSheet('''
            color: #ffffff;
            background-color: #3a3a3a;
            border-radius: 6px;
            padding: 4px 8px;
        ''')
        self.opacity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Container to align label to the right
        opacity_label_container = QHBoxLayout()
        opacity_label_container.setContentsMargins(0, 10, 0, 0)  # Add top margin to push label down
        opacity_label_container.addStretch()
        opacity_label_container.addWidget(self.opacity_label)
        
        opacity_layout.addWidget(self.slider)
        opacity_layout.addWidget(TickBar(self.slider))
        opacity_layout.addLayout(opacity_label_container)
        
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
        
        # Position buttons at top-right corner
        self.close_btn.move(self.width() - self.close_btn.width(), 0)
        self.min_btn.move(self.width() - self.close_btn.width() - self.min_btn.width() - 5, 0)
        
        # Position in bottom right corner
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width()
        y = screen.height() - self.height()
        self.move(x, y)
        
        # System tray setup
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./public/Dimmer.ico'))
        self.tray_icon.setToolTip('Dimmer')
        
        # Create tray menu
        tray_menu = QMenu()
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.quit_app)
        
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
        
    # Override paintEvent to render rounded corners on app window
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Rounded rectangle background
        rect = self.rect()
        color = QColor("#242424")
        radius = 8

        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

    def load_opacity(self):
        default_opacity = 20
        config_file = "./config/opacity_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    return int(data.get('opacity', default_opacity)) # Default opacity to 20% if config not found
            except Exception:
                print("Error loading opacity config")
                pass
        return default_opacity

    def save_opacity(self, opacity: int):
        config_file = "./config/opacity_config.json"
        try:
            with open(config_file, 'w') as f:
                json.dump({'opacity': int(opacity)}, f)
        except Exception:
            print("Error saving opacity config")
            pass

    def on_opacity_changed(self, opacity):
        self.opacity_label.setText(f'{opacity}%')
        self.opacity_changed.emit(opacity * 0.8 / 100) # Cap at 80% opacity
        self.save_opacity(opacity)
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
    
    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == '__main__':
    dimmer = QApplication(sys.argv)
    overlay = Overlay()

    # Create app UI
    app = App()
    overlay.setWindowOpacity(app.load_opacity() * 0.8 / 100)
    app.opacity_changed.connect(overlay.setWindowOpacity)
    app.hide() # Start minimized on start-up

    sys.exit(dimmer.exec())
