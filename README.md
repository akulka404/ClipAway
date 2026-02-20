# ClipAway

### You copy and forget things don't you? ClipAway has you covered!

ClipAway is a lightweight, always-on-top desktop clipboard manager built with Python and PyQt5. It silently monitors your clipboard in the background and keeps a running history of everything you copy — text or files — so you never lose track of what you had on your clipboard.

---

## Features

- **Clipboard History** — Displays your last 10 clipboard entries in a scrollable list, updated in real time (every 100 ms).
- **Persistent Log** — Every clipboard entry is automatically saved with a date and timestamp to `clipboard_log.txt` in the working directory, so your history survives across sessions.
- **File Path Support** — When you copy a file, ClipAway records its full local path so you always know what you had copied.
- **Unobtrusive UI** — The window is nearly invisible (25% opacity) when idle, and becomes fully visible when you hover over it.
- **Draggable Window** — The frameless window can be dragged anywhere on screen to suit your workflow.
- **Lock Position** — Lock the window in place to prevent accidental movement.
- **Minimize & Close** — Standard window controls adapted for the frameless UI.
- **Quick Log Access** — Open `clipboard_log.txt` directly from the app with the "Open Log" button (works on macOS, Windows, and Linux).
- **Always on Top** — The window floats above all other applications so it's always accessible.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language  | Python 3   |
| GUI       | PyQt5      |
| Clipboard | Qt Clipboard API (`QApplication.clipboard()`) |
| Logging   | Python standard library (`os`, `datetime`) |

---

## Prerequisites

- Python 3.6 or higher
- `pip3` package manager

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/akulka404/ClipAway.git
   cd ClipAway
   ```

2. **Install dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

---

## Running the App

```bash
python3 gui.py
```

The ClipAway window will appear on screen. Start copying text or files — ClipAway will automatically track and display your clipboard history.

---

## How It Works

1. A `QTimer` polls the system clipboard every **100 milliseconds**.
2. When new content is detected (text or a file URL), it is prepended to an in-memory `deque` of up to 10 entries.
3. The entry is also written to the top of `clipboard_log.txt` with a `[YYYY-MM-DD HH:MM:SS]` timestamp.
4. The 10 `QTextBrowser` widgets in the scrollable area are refreshed to reflect the current history.

---

## Project Structure

```
ClipAway/
├── gui.py              # Main application — UI setup, clipboard monitoring, logging
├── requirements.txt    # Python dependencies
├── clipboard_log.txt   # Auto-generated clipboard log (created on first copy)
└── README.md           # Project documentation
```

---

## Platform Support

| Platform | Supported | Log File Opens With |
|----------|-----------|---------------------|
| macOS    | ✅        | `open`              |
| Windows  | ✅        | `os.startfile`      |
| Linux    | ✅        | `xdg-open`          |

---

## Contributing

Contributions and suggestions are very welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements — whether it's performance, features, or UI polish.

---

## You're good to go!

ClipAway will keep doing its job quietly in the background. Hover over it whenever you need a peek at your clipboard history.
