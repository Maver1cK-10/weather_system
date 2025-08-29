# main_gui.py

import tkinter as tk
from tkinter import ttk
from monitor_tab import MonitorTab
from predict_tab import PredictTab


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌦️ Smart Weather System")
        self.root.geometry("850x650")
        self.root.config(bg="#f0f8ff")

        # Title
        title_label = tk.Label(
            self.root,
            text="🌍 Weather Monitoring and Prediction App",
            font=("Helvetica", 20, "bold"),
            bg="#f0f8ff",
            fg="#2f3640"
        )
        title_label.pack(pady=20)

        # Tabs
        self.notebook = ttk.Notebook(self.root)

        # Tabs setup
        self.monitor_tab = MonitorTab(self.notebook)
        self.predict_tab = PredictTab(self.notebook)

        self.notebook.add(self.monitor_tab.frame, text="📡 Monitor")
        self.notebook.add(self.predict_tab.frame, text="📊 Predict")
        self.notebook.pack(expand=True, fill='both', padx=15, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
