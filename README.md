# 🔋 BatterySaverApp

A lightweight, cross-platform desktop application that monitors your laptop's battery health by reminding you to unplug at high charges and plug in at low charges.

## ✨ Features
- **High Battery Alerts**: Prevents overcharging (default 95%).
- **Low Battery Alerts**: Protects against deep discharge (default 25%).
- **Live Dashboard**: Real-time battery percentage and time-remaining estimates.
- **Device Detection**: Shows your specific laptop/Mac model in notifications.
- **System Tray Support**: Runs silently in the background with a quick-access menu.
- **Auto-Start**: One-click "Start on boot" feature for Windows, macOS, and Linux.

---

## ⚡ Quick Start

### 🪟 Windows Users
The easiest way is to use the pre-built executable.
1.  **Download**: Get `BatterySaverApp.exe` from the [Releases](https://github.com/Jay0xx/BatterySaverApp/releases) page.
2.  **Run**: Double-click the file to open settings.
3.  **Protect**: Set your limits and click **Save & Minimize**. It will hide in your system tray.

### 🍎 macOS Users
To run the app on Mac:
1.  **Install Python**: Ensure you have Python 3 installed.
2.  **Install Dependencies**: Open Terminal and run:
    ```bash
    pip3 install psutil plyer pystray pillow
    ```
3.  **Launch**: Download `battery_monitor.py` and run:
    ```bash
    python3 battery_monitor.py
    ```
4.  **Package (Optional)**: If you want a `.app` file, run:
    ```bash
    pip3 install pyinstaller
    pyinstaller --onefile --windowed --name BatterySaverApp battery_monitor.py
    ```

---

## 🛠️ Usage & Controls

### Main Dashboard
- **Live Stats**: View your current battery percentage and estimated time remaining.
- **High Threshold**: Get notified when it's time to unplug.
- **Low Threshold**: Get notified when it's time to plug in soon.

### System Tray Menu
Find the battery icon in your taskbar tray (Windows) or Menu Bar (macOS):
- **Right-Click / Click**: Access **Open Settings**, **Pause/Resume**, or **Quit**.
- **Start on Boot**: Enable this in settings to stay protected automatically every time you start your computer.

---

## 👨‍💻 Developer Setup

### 1. Prerequisites
- **Python 3.x**
- **Libraries**:
  ```bash
  pip install psutil plyer pystray pillow
  ```

### 2. Running
```bash
python battery_monitor.py
```

---

## 📝 Troubleshooting
- **No Notifications?** On Windows, check "Focus Assist". On macOS, check "System Settings > Notifications" and ensure Python/BatterySaverApp is allowed.
- **Permission Denied?** On macOS/Linux, you may need to grant permission for the app to access system battery info or for PyInstaller to build the bundle.

---

*Developed with ❤️ to save your battery health.*
