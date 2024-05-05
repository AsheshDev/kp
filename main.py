import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog
import threading
import subprocess
import asyncio
from keystroke_manager import perform_key_event
from file_logger import log_to_file

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Keystroke Simulator")
        self.setup_ui()
        self.running = False
        self.log_message_queue = asyncio.Queue()

    def setup_ui(self):
        self.entry_app_path = tk.Entry(self.root, width=50)
        self.entry_app_path.pack()
        tk.Button(self.root, text="Browse...", command=self.browse_file).pack()
        tk.Button(self.root, text="Start", command=self.toggle_start_stop).pack()
        tk.Button(self.root, text="Test", command=self.test_keystrokes).pack()
        self.log_console = scrolledtext.ScrolledText(self.root, height=10)
        self.log_console.pack()

        self.key_to_press = simpledialog.askstring("Input", "Enter the key to simulate:", parent=self.root)
        self.min_interval = simpledialog.askfloat("Input", "Enter minimum interval (s):", parent=self.root)
        self.max_interval = simpledialog.askfloat("Input", "Enter maximum interval (s):", parent=self.root)

    def browse_file(self):
        self.app_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        self.entry_app_path.delete(0, tk.END)
        self.entry_app_path.insert(0, self.app_path)

    def toggle_start_stop(self):
        if not self.running:
            self.start_keystroke_simulation()
        else:
            self.stop_keystroke_simulation()

    def start_keystroke_simulation(self):
        self.running = True
        self.start_stop_button.config(text="Stop")
        threading.Thread(target=self.send_keystrokes).start()

    def stop_keystroke_simulation(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.log_message_queue.put_nowait(None)

    def send_keystrokes(self):
        subprocess.Popen(self.app_path)
        while self.running:
            perform_key_event(self.key_to_press, self.min_interval, self.max_interval, self.log_message_queue)

    def test_keystrokes(self):
        perform_key_event(self.key_to_press, self.min_interval, self.max_interval, self.log_message_queue)

    async def run_logger(self):
        await log_to_file(self.log_message_queue)

def main():
    root = tk.Tk()
    app = App(root)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run_logger())
    loop.run_until_complete(tk.mainloop())

if __name__ == "__main__":
    main()
