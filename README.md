# 🔋 BatterySaverApp

A lightweight, cross-platform desktop application that monitors your laptop's battery health by reminding you to unplug at high charges and plug in at low charges.

## ✨ Features
- **High Battery Alerts**: Prevents overcharging (default 95%).
- **Low Battery Alerts**: Protects against deep discharge (default 25%).
- **Live Dashboard**: Real-time battery percentage and time-remaining estimates.
- **Device Detection**: Shows your specific laptop/Mac model in notifications.
- **System Tray Support**: Runs silently in the background with a quick-access menu.
- **Auto-Start**: One-click "Start on boot" feature for Windows and macOS.

---

## ⚡ Quick Start (Windows & macOS)

The app can be run by downloading the project directly from the GitHub repository.

1.  **Download**: Click the green **"Code"** button at the top of this page and select **"Download ZIP"**.
2.  **Extract**: Right-click the downloaded folder and extract/unzip it.
3.  **Install Dependencies**: Open your terminal (PowerShell on Windows, Terminal on macOS) and run:
    ```bash
    # Windows
    pip install psutil plyer pystray pillow

    # macOS
    pip3 install psutil plyer pystray pillow
    ```
4.  **Run the App**:
    ```bash
    # Windows
    python battery_monitor.py

    # macOS
    python3 battery_monitor.py
    ```
5.  **Protect**: Set your limits and click **Save & Minimize**. It will hide in your system tray (Windows) or Menu Bar (macOS).

---

## 🛠️ Usage & Controls

### Main Dashboard
- **Live Stats**: View your current battery percentage and estimated time remaining.
- **High Threshold**: Get notified when it's time to unplug.
- **Low Threshold**: Get notified when it's time to plug in soon.

### System Tray / Menu Bar
- **Access**: Right-click the battery icon in your taskbar (Windows) or click the icon in your Menu Bar (macOS).
- **Options**: Access **Open Settings**, **Pause/Resume**, or **Quit**.
- **Start on Boot**: Enable this in settings to stay protected automatically every time you start your computer.

---

## � Packaging (Optional)

To create a standalone app (`.exe` for Windows or `.app` for macOS):

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller  # Windows
    pip3 install pyinstaller # macOS
    ```
2.  Build the bundle:
    ```bash
    pyinstaller --onefile --windowed --name BatterySaverApp battery_monitor.py
    ```
3.  Find your app in the `/dist` folder.

---

## 📝 Troubleshooting
- **No Notifications?** 
  - **Windows**: Check "Focus Assist" settings.
  - **macOS**: Go to "System Settings > Notifications" and ensure Python/BatterySaverApp is allowed to send alerts.
- **Permission Denied?** On macOS, you may need to grant the terminal "Accessibility" or "Full Disk Access" permissions in System Settings if the app cannot read battery data.

---

*Developed with ❤️ to save your battery health.*
