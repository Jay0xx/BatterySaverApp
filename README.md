# 🔋 BatterySaverApp

A lightweight, cross-platform desktop application that monitors your laptop's battery health by reminding you to unplug at high charges and plug in at low charges.

## ✨ Features
- **High Battery Alerts**: Prevents overcharging (default 95%).
- **Low Battery Alerts**: Protects against deep discharge (default 25%).
- **Live Dashboard**: Real-time battery percentage and time-remaining estimates.
- **Device Detection**: Shows your specific laptop model in notifications.
- **System Tray Support**: Runs silently in the background with a quick-access menu.
- **Auto-Start**: One-click "Start on boot" feature.

---

## ⚡ Quick Start (Windows App)

The easiest way to use the app is to use the pre-built executable.

1.  **Download/Locate**: Find `BatterySaverApp.exe` (located in the `dist/` folder).
2.  **Run**: Double-click the file to open the settings window.
3.  **Configure**: Set your preferred high and low thresholds.
4.  **Protect**: Click **Save & Minimize**. The app will now live in your system tray (near the clock).

> **Note**: Windows may show a "SmartScreen" warning since this is a custom-built app. Click **"More info"** and then **"Run anyway"** to proceed.

---

## 🛠️ Usage & Controls

### Main Dashboard
- **Live Stats**: View your current battery percentage and an estimate of how much time you have left.
- **High Threshold**: When your laptop is charging and hits this %, you'll get a reminder to unplug.
- **Low Threshold**: When you are on battery and drop below this %, you'll get a reminder to plug in.

### System Tray Menu
Find the battery icon in your taskbar tray:
- **Right-Click**: Access **Open Settings**, **Pause/Resume**, or **Quit**.
- **Start on Boot**: Check this box in the settings to have the app protect your battery automatically every time you turn on your PC.

---

## 👨‍� Developer Setup (Running from Source)

If you prefer to run the Python script directly or want to modify the code:

### 1. Prerequisites
- **Python 3.x**: [Download here](https://www.python.org/downloads/).
- **Dependencies**: Install the required libraries via terminal:
  ```bash
  pip install psutil plyer pystray pillow
  ```

### 2. Running the Script
```powershell
# Open the settings window
python battery_monitor.py

# Launch directly to tray (no window)
python battery_monitor.py --background
```

### 3. Build your own EXE
If you make changes and want to share your own version:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name BatterySaverApp battery_monitor.py
```

---

## 📝 Troubleshooting
- **No Notifications?** Ensure "Focus Assist" (Windows) or "Do Not Disturb" (macOS) is turned off. 
- **Auto-Start Issues?** If you move the `.exe` file to a new location, reopen the settings and re-check the "Start on boot" box to update the startup path.

---

*Developed with ❤️ to save your battery health.*
