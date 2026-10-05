#!/usr/bin/env python3
"""
Custom Snip/Drag Screenshot Tool for Swinburne SWE40006 Deployment Tasks
Supports multi-monitor setups!
Press your hotkey -> Drag to select area -> Auto-saves!
Type into the terminal anytime while running to adjust prefix, index, or filename!
"""

import os
import glob
import re
import ctypes
import threading
import winsound
import tkinter as tk
from PIL import ImageGrab
import keyboard

# ==============================================================================
# ⚙️ DEFAULT CONFIGURATION
# ==============================================================================
OUTPUT_DIR = r"C:\Users\Admin\Documents\SWE40006\task2\screenshots"
PREFIX = "2.3_"     # Change anytime in code or terminal
HOTKEY = "f9"       # Global key to start snip
BEEP_SOUND = False   # Audio beep feedback
# ==============================================================================

# Global state that can be adjusted interactively in terminal
current_prefix = PREFIX
manual_next_idx = None  # None = auto-detect next available number
manual_exact_name = None  # None = use prefix+idx, or string like "error_log.png"

# Make process DPI aware so coordinates match actual pixels on high-DPI screens
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def get_virtual_screen_rect():
    """Get the bounding rectangle of ALL monitors combined."""
    user32 = ctypes.windll.user32
    x = user32.GetSystemMetrics(76)   # SM_XVIRTUALSCREEN
    y = user32.GetSystemMetrics(77)   # SM_YVIRTUALSCREEN
    w = user32.GetSystemMetrics(78)   # SM_CXVIRTUALSCREEN
    h = user32.GetSystemMetrics(79)   # SM_CYVIRTUALSCREEN
    return x, y, w, h


def get_next_index(directory: str, prefix: str) -> int:
    global manual_next_idx
    if manual_next_idx is not None:
        return manual_next_idx

    os.makedirs(directory, exist_ok=True)
    pattern = os.path.join(directory, f"{prefix}*.png")
    existing = glob.glob(pattern)
    indices = []
    for f in existing:
        basename = os.path.basename(f)
        m = re.search(rf"^{re.escape(prefix)}(\d+)\.png$", basename)
        if m:
            indices.append(int(m.group(1)))
    return max(indices, default=0) + 1


def get_target_filename() -> str:
    global manual_exact_name, manual_next_idx
    if manual_exact_name:
        filename = manual_exact_name if manual_exact_name.endswith(".png") else f"{manual_exact_name}.png"
        full_path = os.path.join(OUTPUT_DIR, filename)
        manual_exact_name = None
        return full_path

    idx = get_next_index(OUTPUT_DIR, current_prefix)
    filename = f"{current_prefix}{idx}.png"
    full_path = os.path.join(OUTPUT_DIR, filename)

    if manual_next_idx is not None:
        manual_next_idx += 1

    return full_path


class SnippingTool:
    def __init__(self):
        # Get virtual screen geometry (all monitors)
        self.vx, self.vy, self.vw, self.vh = get_virtual_screen_rect()

        # Grab full screenshot of ALL screens before showing overlay
        self.screenshot = ImageGrab.grab(
            bbox=(self.vx, self.vy, self.vx + self.vw, self.vy + self.vh),
            all_screens=True
        )

        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove title bar
        self.root.attributes("-alpha", 0.28)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross")

        # Position the window to cover ALL monitors
        self.root.geometry(f"{self.vw}x{self.vh}+{self.vx}+{self.vy}")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray15",
                                width=self.vw, height=self.vh,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 1, 1, outline="#00e5ff", width=2, fill="#00bcd4"
        )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.root.destroy()

        # Calculate bounding box (canvas-relative coordinates)
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        # Ignore tiny accidental clicks (< 10px)
        if (x2 - x1) < 10 or (y2 - y1) < 10:
            print("[-] Snip canceled (selection too small).")
            return

        # Crop from the clean background screenshot
        cropped = self.screenshot.crop((x1, y1, x2, y2))

        # Determine target file
        full_path = get_target_filename()
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        cropped.save(full_path)

        if BEEP_SOUND:
            winsound.Beep(1000, 120)

        print(f"\n[+] [SAVED] {full_path} ({x2 - x1}x{y2 - y1}px)")
        next_preview()


def next_preview():
    if manual_exact_name:
        nxt = manual_exact_name if manual_exact_name.endswith(".png") else f"{manual_exact_name}.png"
    else:
        idx = get_next_index(OUTPUT_DIR, current_prefix)
        nxt = f"{current_prefix}{idx}.png"
    print(f">> Next capture will be: {nxt} | Type command or press [{HOTKEY.upper()}]: ", end="", flush=True)


def terminal_listener():
    global current_prefix, manual_next_idx, manual_exact_name
    while True:
        try:
            cmd = input().strip()
            if not cmd:
                continue

            # Command 1: User enters just a number (e.g. "12") -> sets next index
            if cmd.isdigit():
                manual_next_idx = int(cmd)
                print(f"[!] Next index set to: {manual_next_idx}")

            # Command 2: User enters a full filename or custom name (e.g. "2.4_1" or "error_msg")
            elif "_" in cmd or "." in cmd:
                if cmd.endswith(".png"):
                    manual_exact_name = cmd
                elif any(char.isdigit() for char in cmd):
                    parts = cmd.rsplit("_", 1)
                    if len(parts) == 2 and parts[1].isdigit():
                        current_prefix = parts[0] + "_"
                        manual_next_idx = int(parts[1])
                        print(f"[!] Prefix set to '{current_prefix}', Next index set to {manual_next_idx}")
                    else:
                        manual_exact_name = cmd
                else:
                    manual_exact_name = cmd
                print(f"[!] Next filename configured: {cmd}")

            # Command 3: User enters prefix with or without trailing underscore (e.g. "2.4")
            else:
                p = cmd if cmd.endswith("_") else f"{cmd}_"
                current_prefix = p
                manual_next_idx = None
                print(f"[!] Prefix switched to: '{current_prefix}'")

            next_preview()
        except (EOFError, KeyboardInterrupt):
            break


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    vx, vy, vw, vh = get_virtual_screen_rect()

    print("=" * 65)
    print(" ✂️   SWE40006 INTERACTIVE DRAG & SNIP SCREENSHOT TOOL")
    print("=" * 65)
    print(f" • Output Directory : {OUTPUT_DIR}")
    print(f" • Hotkey           : [{HOTKEY.upper()}] (Press to snip)")
    print(f" • Virtual Screen   : {vw}x{vh} (origin: {vx},{vy})")
    print(" • In Terminal Commands:")
    print("     - Type a number (e.g. 5)      -> sets next file to 2.3_5.png")
    print("     - Type a prefix (e.g. 2.4)     -> switches prefix to 2.4_")
    print("     - Type combined (e.g. 2.4_1)   -> sets prefix to 2.4_ and index to 1")
    print("     - Type custom name (e.g. log)  -> next capture will be log.png")
    print("=" * 65)

    keyboard.add_hotkey(HOTKEY, lambda: SnippingTool())

    t = threading.Thread(target=terminal_listener, daemon=True)
    t.start()

    next_preview()

    try:
        while t.is_alive():
            t.join(timeout=1.0)
    except KeyboardInterrupt:
        print("\nScreenshot tool closed.")


if __name__ == "__main__":
    main()
