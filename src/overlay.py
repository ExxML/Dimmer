import sys
import ctypes
import signal
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget
from app import App

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window flags for overlay behavior
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput  # Click-through
        )
        
        # Window setup
        self.setGeometry(QApplication.primaryScreen().geometry())
        self.setWindowOpacity(0.5)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.show()
        
        # Set display affinity to exclude overlay from screen capture (Windows 10+)
        hwnd = int(self.winId())
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        result = ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        if result == 0:
            print("Warning: SetWindowDisplayAffinity failed. May appear in screenshots.")

if __name__ == '__main__':
    dimmer = QApplication(sys.argv)
    overlay = Overlay()
    
    # Create app UI
    app = App()
    app.opacity_changed.connect(overlay.setWindowOpacity)
    app.show()
    
    sys.exit(dimmer.exec())