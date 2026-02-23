import os
import json
import sys
import threading
import time
import argparse
import platform
import subprocess
import psutil
from plyer import notification
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox, ttk

# --- Constants & Configuration ---
APP_NAME = "BatterySaverApp"
CONFIG_FILE = os.path.expanduser("~/.batterysaver_config.json")

DEFAULT_CONFIG = {
    "threshold": 95,
    "low_threshold": 25,
    "interval": 30,
    "message": "{device_model} battery at {percent}%! Unplug charger to preserve battery health.",
    "low_message": "{device_model} battery at {percent}%! Plug in soon to avoid deep discharge.",
    "start_on_boot": False
}

def get_device_model():
    """Detects the laptop/PC/Mac model name cross-platform."""
    system = platform.system()
    try:
        if system == "Windows":
            cmd = "wmic csproduct get name"
            output = subprocess.check_output(cmd, shell=True).decode().split('\n')
            if len(output) > 1:
                return output[1].strip()
        elif system == "Darwin":
            return subprocess.check_output(["sysctl", "-n", "hw.model"]).decode().strip()
        elif system == "Linux":
            for path in ["/sys/class/dmi/id/product_name", "/sys/class/dmi/id/model_name"]:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        return f.read().strip()
    except Exception:
        pass
    return "Unknown device"

class ConfigManager:
    @staticmethod
    def load():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                return DEFAULT_CONFIG
        return DEFAULT_CONFIG

    @staticmethod
    def save(config):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

# --- OS Specific Auto-Start ---
def set_autostart(enabled):
    system = platform.system()
    script_path = os.path.abspath(sys.argv[0])
    
    if system == "Windows":
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}" --background')
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Windows Registry Error: {e}")

    elif system == "Darwin":  # macOS
        plist_path = os.path.expanduser(f"~/Library/LaunchAgents/com.{APP_NAME.lower()}.plist")
        if enabled:
            content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{APP_NAME.lower()}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{script_path}</string>
        <string>--background</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
            try:
                os.makedirs(os.path.dirname(plist_path), exist_ok=True)
                with open(plist_path, "w") as f:
                    f.write(content)
            except Exception as e:
                print(f"macOS LaunchAgent Error: {e}")
        else:
            if os.path.exists(plist_path):
                os.remove(plist_path)

    elif system == "Linux":
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_dir, f"{APP_NAME.lower()}.desktop")
        if enabled:
            try:
                os.makedirs(autostart_dir, exist_ok=True)
                content = f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Exec={sys.executable} {script_path} --background
Terminal=false
"""
                with open(desktop_file, "w") as f:
                    f.write(content)
            except Exception as e:
                print(f"Linux Autostart Error: {e}")
        else:
            if os.path.exists(desktop_file):
                os.remove(desktop_file)

# --- Core Logic & Tray ---
class BatterySaverApp:
    def __init__(self, config, start_minimized=False):
        self.config = config
        self.device_model = get_device_model()
        self.stop_event = threading.Event()
        self.paused = False
        self.notified_high_this_session = False
        self.notified_low_this_session = False
        self.icon = None
        self.gui = None
        
        # UI Refresh variables
        self.stat_percent = None
        self.stat_time = None
        self.stat_health = "Health stats limited on this OS"

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()

        if start_minimized:
            self.run_tray()
        else:
            self.show_gui()

    def create_image(self):
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(image)
        d.rectangle([10, 20, 50, 50], outline="white", width=3)
        d.rectangle([50, 30, 55, 40], fill="white")
        d.rectangle([14, 24, 46, 46], fill="#00FF00")
        return image

    def monitor_loop(self):
        while not self.stop_event.is_set():
            if not self.paused:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    is_plugged = battery.power_plugged
                    
                    # High Battery Logic
                    if is_plugged and percent >= self.config["threshold"]:
                        if not self.notified_high_this_session:
                            self.send_notif(self.config["message"], percent)
                            self.notified_high_this_session = True
                    elif not is_plugged:
                        self.notified_high_this_session = False
                        
                    # Low Battery Logic
                    if not is_plugged and percent <= self.config["low_threshold"]:
                        if not self.notified_low_this_session:
                            self.send_notif(self.config["low_message"], percent)
                            self.notified_low_this_session = True
                    elif is_plugged:
                        self.notified_low_this_session = False
            
            self.stop_event.wait(self.config["interval"])

    def send_notif(self, template, percent):
        try:
            msg = template.format(percent=percent, device_model=self.device_model)
        except KeyError:
            msg = f"{self.device_model} battery at {percent}%!"
            
        notification.notify(
            title="Battery Alert",
            message=msg,
            app_name=APP_NAME,
            timeout=10
        )

    def get_stats(self):
        battery = psutil.sensors_battery()
        if not battery:
            return "No battery detected", "N/A", "N/A"
        
        percent = f"{battery.percent}%"
        plugged = " (Charging)" if battery.power_plugged else " (Discharging)"
        
        if battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            time_left = "Calculating..."
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            time_left = "Unlimited (Plugged in)"
        else:
            h, m = divmod(battery.secsleft // 60, 60)
            time_left = f"{h}h {m}m remaining"
            
        return percent + plugged, time_left, self.stat_health

    def show_gui(self):
        if self.gui:
            self.gui.deiconify()
            return

        self.gui = tk.Tk()
        self.gui.title(APP_NAME)
        self.gui.geometry("500x650")
        self.gui.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Stat.TLabel", font=("Segoe UI", 10, "bold"), foreground="#2980b9")

        main_scroll = tk.Canvas(self.gui)
        scrollbar = ttk.Scrollbar(self.gui, orient="vertical", command=main_scroll.yview)
        scrollable_frame = ttk.Frame(main_scroll)

        scrollable_frame.bind("<Configure>", lambda e: main_scroll.configure(scrollregion=main_scroll.bbox("all")))
        main_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_scroll.configure(yscrollcommand=scrollbar.set)

        padding_frame = ttk.Frame(scrollable_frame, padding="20")
        padding_frame.pack(fill=tk.BOTH, expand=True)

        # --- LIVE STATS ---
        ttk.Label(padding_frame, text="Live Battery Information", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        stat_box = ttk.LabelFrame(padding_frame, padding="15")
        stat_box.pack(fill=tk.X, pady=(0, 20))

        self.lbl_percent = ttk.Label(stat_box, text="Charge: --", style="Stat.TLabel")
        self.lbl_percent.pack(anchor=tk.W)
        self.lbl_time = ttk.Label(stat_box, text="Time: --")
        self.lbl_time.pack(anchor=tk.W)
        self.lbl_health = ttk.Label(stat_box, text=f"Health: {self.stat_health}", font=("Segoe UI", 9, "italic"))
        self.lbl_health.pack(anchor=tk.W, pady=(5,0))

        # --- DEVICE INFO ---
        ttk.Label(padding_frame, text=f"Detected Device: {self.device_model}", font=("Segoe UI", 9, "italic")).pack(anchor=tk.W, pady=(0, 20))
        ttk.Separator(padding_frame, orient='horizontal').pack(fill=tk.X, pady=10)

        # --- HIGH BATTERY SETTINGS ---
        ttk.Label(padding_frame, text="High Battery Alert (Plugged In)", style="Header.TLabel").pack(anchor=tk.W, pady=10)
        
        high_val = tk.IntVar(value=self.config["threshold"])
        high_label = tk.StringVar(value=f"Notify at: {high_val.get()}%")
        ttk.Label(padding_frame, textvariable=high_label).pack(anchor=tk.W)
        ttk.Scale(padding_frame, from_=50, to=100, variable=high_val, orient=tk.HORIZONTAL, command=lambda x: high_label.set(f"Notify at: {high_val.get()}%")).pack(fill=tk.X, pady=5)

        # --- LOW BATTERY SETTINGS ---
        ttk.Label(padding_frame, text="Low Battery Alert (On Battery)", style="Header.TLabel").pack(anchor=tk.W, pady=(20, 10))
        
        low_val = tk.IntVar(value=self.config["low_threshold"])
        low_label_var = tk.StringVar(value=f"Notify at: {low_val.get()}%")
        ttk.Label(padding_frame, textvariable=low_label_var).pack(anchor=tk.W)
        ttk.Scale(padding_frame, from_=5, to=50, variable=low_val, orient=tk.HORIZONTAL, command=lambda x: low_label_var.set(f"Notify at: {low_val.get()}%")).pack(fill=tk.X, pady=5)

        # --- GENERAL SETTINGS ---
        ttk.Separator(padding_frame, orient='horizontal').pack(fill=tk.X, pady=20)
        
        ttk.Label(padding_frame, text="Poll Interval (seconds):").pack(anchor=tk.W)
        interval_entry = ttk.Entry(padding_frame)
        interval_entry.insert(0, str(self.config["interval"]))
        interval_entry.pack(fill=tk.X, pady=5)

        boot_var = tk.BooleanVar(value=self.config["start_on_boot"])
        ttk.Checkbutton(padding_frame, text="Start on boot", variable=boot_var).pack(anchor=tk.W, pady=10)

        def save_settings():
            try:
                self.config["threshold"] = high_val.get()
                self.config["low_threshold"] = low_val.get()
                self.config["interval"] = int(interval_entry.get())
                self.config["start_on_boot"] = boot_var.get()
                ConfigManager.save(self.config)
                set_autostart(self.config["start_on_boot"])
                self.minimize_to_tray()
            except ValueError:
                messagebox.showerror("Error", "Interval must be a number")

        btn_frame = ttk.Frame(padding_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Save & Minimize", command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Quit App", command=self.quit_app).pack(side=tk.LEFT, padx=5)

        main_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def update_stats_loop():
            if self.gui and self.gui.winfo_exists():
                p, t, h = self.get_stats()
                self.lbl_percent.config(text=f"Charge: {p}")
                self.lbl_time.config(text=f"Estimate: {t}")
                self.gui.after(5000, update_stats_loop)

        update_stats_loop()
        self.gui.mainloop()

    def minimize_to_tray(self):
        if self.gui: self.gui.withdraw()
        if not self.icon: threading.Thread(target=self.run_tray, daemon=True).start()

    def run_tray(self):
        def toggle_pause(icon, item): self.paused = not self.paused
        menu = pystray.Menu(
            item('Open Settings', lambda: self.gui.after(0, self.show_gui)),
            item('Pause/Resume', toggle_pause, checked=lambda item: self.paused),
            item('Quit', self.quit_app)
        )
        self.icon = pystray.Icon(APP_NAME, self.create_image(), APP_NAME, menu)
        self.icon.run()

    def quit_app(self, icon=None, item=None):
        self.stop_event.set()
        if self.icon: self.icon.stop()
        if self.gui: self.gui.destroy()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--background", action="store_true", help="Start directly in tray")
    args = parser.parse_args()
    app = BatterySaverApp(ConfigManager.load(), start_minimized=args.background)

# --- DOCUMENTATION ---
"""
Installation:
1. Python 3.x
2. pip install psutil plyer pystray pillow

Packaging:
pyinstaller --onefile --windowed --name BatterySaverApp battery_monitor.py

Testing:
1. Low Battery: Set low threshold to 1-2% below current while unplugged.
2. High Battery: Set high threshold to 1-2% above current while plugged.
3. Live Stats: Open GUI and watch the 'Charge' and 'Estimate' update every 5 seconds.

Limitations:
- Battery health (cycles/wear) is not reliably exposed by the cross-platform psutil library.
- MacOS/Linux auto-start requires specific file permissions.
"""
