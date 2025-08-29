import tkinter as tk
import requests
from tkinter import messagebox

class MonitorTab:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="#f0f8ff")
        self.frame.pack(fill="both", expand=True)

        # Header
        self.title = tk.Label(
            self.frame,
            text="📡 Real-time Weather Monitoring",
            font=("Helvetica", 20, "bold"),
            bg="#f0f8ff",
            fg="#1e272e"
        )
        self.title.pack(pady=20)

        # Weather Info Card
        self.info_card = tk.Label(
            self.frame,
            text="Fetching live data...",
            font=("Helvetica", 14),
            bg="#dff9fb",
            fg="#34495e",
            bd=2,
            relief="groove",
            padx=10,
            pady=10,
            width=50,
            height=5,
            anchor="center",
            justify="center",
            wraplength=400
        )
        self.info_card.pack(pady=20)

        # Refresh Button
        self.refresh_btn = tk.Button(
            self.frame,
            text="🔄 Refresh",
            command=self.fetch_weather,
            font=("Helvetica", 12, "bold"),
            bg="#00a8ff",
            fg="white",
            width=15,
            relief="raised",
            bd=3
        )
        self.refresh_btn.pack(pady=10)

        # Auto-fetch on load
        self.fetch_weather()

    def fetch_weather(self):
        city = "Pune"
        api_key = "demo"  # Replace with your API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                self.info_card.config(text=f"Error: {data.get('message', 'Unknown error')}")
                return

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            description = data["weather"][0]["description"].capitalize()

            self.info_card.config(
                text=(
                    f"🌡️ Temperature: {temp} °C\n"
                    f"💧 Humidity: {humidity}%\n"
                    f"📈 Pressure: {pressure} hPa\n"
                    f"🌬️ Wind Speed: {wind} m/s\n"
                    f"☁️ Condition: {description}"
                )
            )

        except Exception as e:
            messagebox.showerror("API Error", f"Failed to fetch weather data:\n{str(e)}")