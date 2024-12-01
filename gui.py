# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pyperclip
from collections import deque
from datetime import datetime


class Ui_Form(object):
    def __init__(self):
        self.clipboard_history = deque(maxlen=10)  # Store last 10 clipboard entries
        self.log_file = "clipboard_log.txt"

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 605)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 581))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Initialize UI elements
        self.text_browsers = []
        self.initialize_text_browsers()

    def initialize_text_browsers(self):
        # Create 10 QTextBrowsers dynamically and add to the layout
        for _ in range(10):
            text_browser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
            text_browser.setObjectName(f"textBrowser_{len(self.text_browsers)}")
            self.text_browsers.append(text_browser)
            self.dynamicLayout.addWidget(text_browser)

    def update_clipboard(self):
        try:
            content = pyperclip.paste()
            if content and (not self.clipboard_history or self.clipboard_history[-1] != content):
                # Add new content to the clipboard history
                self.clipboard_history.append(content)
                self.log_clipboard(content)
                self.update_text_browsers()
        except Exception as e:
            print(f"Error accessing clipboard: {e}")

    def log_clipboard(self, content):
        with open(self.log_file, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {content}\n")

    def update_text_browsers(self):
        # Update each QTextBrowser with the corresponding clipboard history item
        for i, text_browser in enumerate(self.text_browsers):
            if i < len(self.clipboard_history):
                text_browser.setText(self.clipboard_history[i])
            else:
                text_browser.clear()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ClipAway"))
        self.label.setText(_translate("Form", "ClipAway- Clipboard History"))


if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import QTimer

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)

    # Periodically check the clipboard for updates
    def check_clipboard():
        ui.update_clipboard()

    timer = QTimer()
    timer.timeout.connect(check_clipboard)
    timer.start(100)  # Check clipboard every 100ms

    Form.show()
    sys.exit(app.exec_())