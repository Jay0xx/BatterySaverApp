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

The app can be run by downloading the project directly from the GitHub repository.

1.  **Download**: Click the green **"Code"** button at the top of this page and select **"Download ZIP"**.
2.  **Extract**: Right-click the downloaded folder and "Extract All".
3.  **Install dependencies**: Open your terminal and run:
    ```bash
    pip install psutil plyer pystray pillow
    ```
4.  **Run**: Double-click `battery_monitor.py` or run `python battery_monitor.py` in your terminal to open the settings.
5.  **Protect**: Set your limits and click **Save & Minimize**. It will hide in your system tray.

> **Note for Windows Users**: If you have built your own `.exe` using the developer instructions below, you can run that directly without needing to install Python libraries first.

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
