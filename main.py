import time
import threading
import tkinter as tk
from tkinter import messagebox
from pynput.mouse import Controller, Button
from pynput import keyboard

# Initialize mouse controller
mouse = Controller()
clicking = False  # Flag to control clicking

def start_clicking():
    """Starts auto-clicking at the current cursor position"""
    global clicking
    if clicking:
        return  # Already running

    try:
        delay = int(entry_delay.get())
        clicks = int(entry_clicks.get())

        if delay < 1:
            messagebox.showerror("Error", "Delay must be at least 1 ms.")
            return

        clicking = True
        threading.Thread(target=click_loop, args=(delay, clicks), daemon=True).start()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def click_loop(delay, clicks):
    """Executes the clicking loop at the current cursor position"""
    global clicking
    messagebox.showinfo("Auto Clicker", "Move your mouse to the target position.\nClicking will start in 3 seconds.")

    time.sleep(3)  # Give the user time to place the cursor
    for _ in range(clicks):
        if not clicking:
            break
        mouse.click(Button.left)
        time.sleep(delay / 1000)  # Convert milliseconds to seconds

    clicking = False
    messagebox.showinfo("Auto Clicker", "Clicking Finished!")  # Notify when done

def stop_clicking():
    """Stops clicking when called"""
    global clicking
    clicking = False

def on_hotkey(key):
    """Handles shortcut keys"""
    if key == keyboard.Key.f6:  # Press F6 to start clicking
        start_clicking()
    elif key == keyboard.Key.f7:  # Press F7 to stop clicking
        stop_clicking()

# Start keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_hotkey)
listener.start()

# Create GUI
root = tk.Tk()
root.title("Mayur Auto Clicker")
root.geometry("300x200")
root.resizable(False, False)

# Labels and Entry Fields
tk.Label(root, text="Delay (ms):").pack()
entry_delay = tk.Entry(root)
entry_delay.pack()

tk.Label(root, text="Number of Clicks:").pack()
entry_clicks = tk.Entry(root)
entry_clicks.pack()

# Start and Stop Buttons
btn_start = tk.Button(root, text="Start Clicking (F6)", command=start_clicking, bg="green", fg="white")
btn_start.pack(pady=5)

btn_stop = tk.Button(root, text="Stop Clicking (F7)", command=stop_clicking, bg="red", fg="white")
btn_stop.pack(pady=5)

# Run GUI
root.mainloop()
