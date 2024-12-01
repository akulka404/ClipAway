import sys
import pyperclip
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from collections import deque
from datetime import datetime

# Configuration
CLIPBOARD_LIMIT = 10
LOG_FILE = "clipboard_log.txt"

class ClipboardMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clipboard_history = deque(maxlen=CLIPBOARD_LIMIT)
        self.init_ui()
        self.setup_clipboard_listener()

    def init_ui(self):
        # Set up main window
        self.setWindowTitle("Clipboard Monitor")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set up layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Label to display clipboard history
        self.history_label = QLabel("", self)
        self.history_label.setStyleSheet("color: white; background-color: black; padding: 10px;")
        self.history_label.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.history_label)

        self.update_ui()

    def setup_clipboard_listener(self):
        # Use a QTimer to poll the clipboard periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(100)  # Check clipboard every 100ms

    def check_clipboard(self):
        try:
            current_content = pyperclip.paste()
            if current_content and (not self.clipboard_history or self.clipboard_history[-1] != current_content):
                self.clipboard_history.append(current_content)
                self.log_clipboard(current_content)
                self.update_ui()
        except Exception as e:
            print(f"Error checking clipboard: {e}")

    def log_clipboard(self, content):
        with open(LOG_FILE, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {content}\n")

    def update_ui(self):
        self.history_label.setText("\n".join(self.clipboard_history))

    def mousePressEvent(self, event):
        # Allow dragging of the floating window
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        # Allow dragging of the floating window
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardMonitor()
    window.show()
    sys.exit(app.exec_())
