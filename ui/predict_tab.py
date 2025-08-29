import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PredictTab:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="#eef2f3")
        self.frame.pack(fill="both", expand=True)

        # Header
        title = tk.Label(
            self.frame,
            text="Rainfall Prediction System",
            font=("Helvetica", 20, "bold"),
            bg="#eef2f3",
            fg="#2f3542"
        )
        title.pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self.frame, bg="#dff9fb", bd=2, relief="ridge")
        input_frame.pack(pady=10, padx=20)

        self.temp_entry = self._add_input(input_frame, "Temperature (°C):")
        self.humidity_entry = self._add_input(input_frame, "Humidity (%):")
        self.pressure_entry = self._add_input(input_frame, "Pressure (hPa):")
        self.wind_entry = self._add_input(input_frame, "Wind Speed (m/s):")

        # Button Frame
        btn_frame = tk.Frame(self.frame, bg="#eef2f3")
        btn_frame.pack(pady=10)

        predict_btn = tk.Button(
            btn_frame,
            text="Predict",
            command=self.predict_weather,
            bg="#1dd1a1",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=12
        )
        predict_btn.pack(side="left", padx=10)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields,
            bg="#ff6b6b",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=12
        )
        clear_btn.pack(side="left", padx=10)

        # Result Card
        self.result_card = tk.Label(
            self.frame,
            text="Awaiting prediction...",
            font=("Helvetica", 14),
            bg="#f1f2f6",
            fg="#1e272e",
            bd=2,
            relief="groove",
            wraplength=600,
            justify="left",
            padx=10,
            pady=10
        )
        self.result_card.pack(pady=15)

        # Toggle Button for Graph
        self.graph_toggle_btn = tk.Button(
            self.frame,
            text="Show Graph 📊",
            command=self.toggle_graph,
            bg="#0984e3",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15
        )
        self.graph_toggle_btn.pack(pady=5)

        # Graph Frame (Initially Hidden)
        self.graph_frame = tk.Frame(self.frame, bg="#eef2f3")
        self.graph_frame.pack_forget()

        self.last_predictions = None

    def _add_input(self, parent, label_text):
        frame = tk.Frame(parent, bg="#dff9fb")
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text, font=("Helvetica", 12, "bold"), bg="#dff9fb")
        label.pack(anchor="w")
        entry = tk.Entry(frame, font=("Helvetica", 12), width=25, bd=1, relief="solid")
        entry.pack()
        return entry

    def clear_fields(self):
        self.temp_entry.delete(0, tk.END)
        self.humidity_entry.delete(0, tk.END)
        self.pressure_entry.delete(0, tk.END)
        self.wind_entry.delete(0, tk.END)
        self.result_card.config(text="Awaiting prediction...")
        self.last_predictions = None
        self.graph_frame.pack_forget()
        self.graph_toggle_btn.config(text="Show Graph 📊")

    def predict_weather(self):
        try:
            temp = float(self.temp_entry.get())
            humidity = float(self.humidity_entry.get())
            pressure = float(self.pressure_entry.get())
            wind = float(self.wind_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        try:
            df = pd.DataFrame([[temp, humidity, pressure, wind]],
                              columns=["temp", "humidity", "sealevelpressure", "windspeed"])

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models")

            scaler = joblib.load(os.path.join(model_path, "scaler.pkl"))
            logistic_model = joblib.load(os.path.join(model_path, "logistic_model.pkl"))
            linear_model = joblib.load(os.path.join(model_path, "linear_model.pkl"))
            rf_model = joblib.load(os.path.join(model_path, "random_forest_model.pkl"))

            scaled = scaler.transform(df)

            is_rain = logistic_model.predict(scaled)[0]
            rain_text = "🌧️ Yes, carry an umbrella!" if is_rain else "☀️ No rain expected."

            lin_pred = linear_model.predict(scaled)[0]
            rf_pred = rf_model.predict(df)[0]

            cloud_cover = "Overcast ☁️" if is_rain else "Clear 🌤️"

            result = (
                f"Rain Expected? → {rain_text}\n\n"
                f"Linear Regression Estimate: {lin_pred:.2f} mm\n"
                f"Random Forest Estimate: {rf_pred:.2f} mm\n"
                f"Cloud Cover: {cloud_cover}"
            )
            self.result_card.config(text=result)

            self.last_predictions = [lin_pred, rf_pred]
            self.graph_toggle_btn.config(text="Show Graph 📊")
            self.graph_frame.pack_forget()

        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    def toggle_graph(self):
        if self.graph_frame.winfo_ismapped():
            self.graph_frame.pack_forget()
            self.graph_toggle_btn.config(text="Show Graph 📊")
        else:
            self._plot_graph()
            self.graph_frame.pack(pady=10)
            self.graph_toggle_btn.config(text="Hide Graph ❌")

    def _plot_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if not self.last_predictions:
            return

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        model_names = ['Linear Regression', 'Random Forest']
        colors = ['#74b9ff', '#00cec9']

        ax.bar(model_names, self.last_predictions, color=colors)
        ax.set_ylabel('Rainfall (mm)')
        ax.set_title('Model-wise Rainfall Prediction')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)
