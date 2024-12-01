import tkinter as tk
import pyperclip
import keyboard
import time
import os
from datetime import datetime
from collections import deque

# Configuration
CLIPBOARD_LIMIT = 10
LOG_FILE = "clipboard_log.txt"

# Queue to maintain clipboard history
clipboard_history = deque(maxlen=CLIPBOARD_LIMIT)

# Function to log clipboard content to file
def log_clipboard(content):
    with open(LOG_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {content}\n")

# Function to update floating widget
def update_widget():
    display_text = "\n".join(clipboard_history)
    widget_label.config(text=display_text)

# Function to handle clipboard updates
def update_clipboard():
    try:
        content = pyperclip.paste()
        if content and (not clipboard_history or clipboard_history[-1] != content):
            clipboard_history.append(content)
            if len(clipboard_history) == CLIPBOARD_LIMIT:
                popped = clipboard_history.popleft()
                log_clipboard(popped)
            update_widget()
    except Exception as e:
        print(f"Error updating clipboard: {e}")

# Keyboard listener for cmd+c and cmd+x
def clipboard_listener():
    while True:
        if keyboard.is_pressed("cmd+c") or keyboard.is_pressed("cmd+x"):
            time.sleep(0.1)  # Avoid duplicate reads
            update_clipboard()

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Clipboard Monitor")
root.geometry("300x200")
root.attributes("-topmost", True)  # Keep on top
root.resizable(False, False)

# Create a label to display clipboard history
widget_label = tk.Label(root, text="", justify="left", anchor="w")
widget_label.pack(fill="both", expand=True)

# Start clipboard listener in a separate thread
import threading
listener_thread = threading.Thread(target=clipboard_listener, daemon=True)
listener_thread.start()

# Start the Tkinter main loop
root.mainloop()