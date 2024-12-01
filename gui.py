# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from collections import deque
from datetime import datetime
import os
import subprocess


class Ui_Form(object):
    def __init__(self):
        self.clipboard_history = deque(maxlen=10)  # Store last 10 clipboard entries
        self.log_file = "clipboard_log.txt"
        self.position_locked = False  # Flag for lock position

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 605)
        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        # Form.setWindowOpacity(0.5)  # Start with 50% transparency
        self.Form = Form

        # Central widget and layout
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 581))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Header with controls
        self.header_layout = QtWidgets.QHBoxLayout()

        self.lock_button = QtWidgets.QPushButton("Lock", self.verticalLayoutWidget)
        self.lock_button.setObjectName("lock_button")
        self.lock_button.clicked.connect(self.toggle_lock_position)

        self.minimize_button = QtWidgets.QPushButton("Minimize", self.verticalLayoutWidget)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.clicked.connect(self.minimize_window)

        self.close_button = QtWidgets.QPushButton("Close", self.verticalLayoutWidget)
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(self.close_application)

        self.open_log_button = QtWidgets.QPushButton("Open Log", self.verticalLayoutWidget)
        self.open_log_button.setObjectName("open_log_button")
        self.open_log_button.clicked.connect(self.open_log_file)

        self.header_layout.addWidget(self.lock_button)
        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.close_button)
        self.header_layout.addWidget(self.open_log_button)
        self.verticalLayout.addLayout(self.header_layout)

        # Label for title
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        # Scrollable area
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 377, 529))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.dynamicLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.dynamicLayout.setObjectName("dynamicLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # Initialize UI elements
        self.text_browsers = []
        self.initialize_text_browsers()

        # Hover event filters
        Form.setAttribute(QtCore.Qt.WA_Hover)
        Form.setMouseTracking(True)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def initialize_text_browsers(self):
        for _ in range(10):
            text_browser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
            text_browser.setObjectName(f"textBrowser_{len(self.text_browsers)}")
            self.text_browsers.append(text_browser)
            self.dynamicLayout.addWidget(text_browser)

    def update_clipboard(self):
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            mime_data = clipboard.mimeData()
            
            if mime_data.hasUrls():
                urls = mime_data.urls()
                if urls:
                    content = urls[0].toLocalFile()  # Get the full local file path
            elif mime_data.hasText():
                content = clipboard.text()
            else:
                return  # Ignore unsupported data

            # Avoid duplicates
            if not self.clipboard_history or self.clipboard_history[0] != content:
                self.clipboard_history.appendleft(content)
                self.log_clipboard(content)
                self.update_ui()
        except Exception as e:
            print(f"Error accessing clipboard: {e}")

    def log_clipboard(self, content):
        try:
            # Read existing content
            existing_content = ""
            if os.path.exists(self.log_file):
                with open(self.log_file, "r", encoding='utf-8') as file:
                    existing_content = file.read()
            
            # Prepend new entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = f"[{timestamp}] {content}\n"
            
            # Write updated content
            with open(self.log_file, "w", encoding='utf-8') as file:
                file.write(new_entry + existing_content)
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def update_ui(self):
        # Update all text browsers based on clipboard history
        for i, text_browser in enumerate(self.text_browsers):
            if i < len(self.clipboard_history):
                text_browser.setText(self.clipboard_history[i])
            else:
                text_browser.clear()

    def toggle_lock_position(self):
        self.position_locked = not self.position_locked
        self.lock_button.setText("Unlock" if self.position_locked else "Lock")

    def minimize_window(self):
        self.Form.showMinimized()

    def close_application(self):
        QtWidgets.QApplication.quit()

    def open_log_file(self):
        if os.name == "posix":
            subprocess.call(["open", self.log_file])  # macOS
        elif os.name == "nt":
            os.startfile(self.log_file)  # Windows
        else:
            subprocess.call(["xdg-open", self.log_file])  # Linux

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ClipAway"))
        self.label.setText(_translate("Form", "ClipAway- Clipboard History"))


class MainForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.25)

    def mouseMoveEvent(self, event):
        self.setWindowOpacity(1.0)  # Full opacity on hover
        super().mouseMoveEvent(event)
    
    def enterEvent(self, event):
        self.setWindowOpacity(1.0)  # Set opacity to 100% when mouse enters
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setWindowOpacity(0.25)  # Set opacity back to 50% when mouse leaves
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if not self.position_locked and event.button() == QtCore.Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if not self.position_locked and event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)


if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import QTimer

    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()

    # Periodically check the clipboard for updates
    def check_clipboard():
        form.update_clipboard()

    timer = QTimer()
    timer.timeout.connect(check_clipboard)
    timer.start(100)  # Check clipboard every 100ms

    form.show()
    sys.exit(app.exec_())