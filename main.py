import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLineEdit, QFrame, 
                             QGraphicsDropShadowEffect, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QIcon, QColor
from dotenv import load_dotenv

# Get directory containing main.py
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 200, 420, 600)
        self.setFixedSize(420, 600)
        
        # Set app window icon
        icon_path = os.path.join(base_dir, "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Fallback to old icon name if png not copied
            fallback_icon = os.path.join(base_dir, "icon.jpg")
            if os.path.exists(fallback_icon):
                self.setWindowIcon(QIcon(fallback_icon))

        # Setup main layouts
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Glassmorphic container card
        self.card = QFrame(self)
        self.card.setObjectName("glass_card")
        
        # Soft shadow for glass card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 45))
        shadow.setOffset(0, 8)
        self.card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 25, 20, 25)
        card_layout.setSpacing(12)
        
        # 1. Title (Stylized distinctly with Montserrat/Century Gothic feel)
        self.title_label = QLabel("W E A T H E R", self.card)
        self.title_label.setObjectName("app_title")
        self.title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title_label)
        
        # 2. Input
        self.city_name = QLineEdit(self.card)
        self.city_name.setPlaceholderText("Enter City Name...")
        self.city_name.setAlignment(Qt.AlignCenter)
        self.city_name.setObjectName("city_input")
        card_layout.addWidget(self.city_name)
        
        # 3. Button
        self.get_weather_button = QPushButton("Get Weather", self.card)
        self.get_weather_button.setObjectName("search_btn")
        self.get_weather_button.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.get_weather_button)
        
        # 4. Results Container (wrapped for animation)
        self.results_container = QWidget(self.card)
        self.results_container.setObjectName("results_container")
        results_layout = QVBoxLayout(self.results_container)
        results_layout.setContentsMargins(0, 5, 0, 0)
        results_layout.setSpacing(10)
        
        self.emoji_label = QLabel(self.results_container)
        self.emoji_label.setObjectName("emoji_label")
        self.emoji_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.emoji_label)
        
        self.temperature_label = QLabel(self.results_container)
        self.temperature_label.setObjectName("temp_label")
        self.temperature_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.temperature_label)
        
        self.description_label = QLabel(self.results_container)
        self.description_label.setObjectName("desc_label")
        self.description_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.description_label)
        
        # 5. Details Card (Feels Like, Humidity, Wind)
        self.details_card = QFrame(self.results_container)
        self.details_card.setObjectName("details_card")
        details_layout = QHBoxLayout(self.details_card)
        details_layout.setContentsMargins(10, 15, 10, 15)
        details_layout.setSpacing(5)
        
        # Feels Like block
        feels_layout = QVBoxLayout()
        self.feels_icon = QLabel("🌡️", self.details_card)
        self.feels_icon.setAlignment(Qt.AlignCenter)
        self.feels_icon.setStyleSheet("font-size: 20px;")
        self.feels_like_val = QLabel("--", self.details_card)
        self.feels_like_val.setAlignment(Qt.AlignCenter)
        self.feels_like_val.setObjectName("detail_value")
        self.feels_lbl = QLabel("FEELS LIKE", self.details_card)
        self.feels_lbl.setAlignment(Qt.AlignCenter)
        self.feels_lbl.setObjectName("detail_label")
        feels_layout.addWidget(self.feels_icon)
        feels_layout.addWidget(self.feels_like_val)
        feels_layout.addWidget(self.feels_lbl)
        
        # Humidity block
        humidity_layout = QVBoxLayout()
        self.humidity_icon = QLabel("💧", self.details_card)
        self.humidity_icon.setAlignment(Qt.AlignCenter)
        self.humidity_icon.setStyleSheet("font-size: 20px;")
        self.humidity_val = QLabel("--", self.details_card)
        self.humidity_val.setAlignment(Qt.AlignCenter)
        self.humidity_val.setObjectName("detail_value")
        self.humidity_lbl = QLabel("HUMIDITY", self.details_card)
        self.humidity_lbl.setAlignment(Qt.AlignCenter)
        self.humidity_lbl.setObjectName("detail_label")
        humidity_layout.addWidget(self.humidity_icon)
        humidity_layout.addWidget(self.humidity_val)
        humidity_layout.addWidget(self.humidity_lbl)
        
        # Wind block
        wind_layout = QVBoxLayout()
        self.wind_icon = QLabel("💨", self.details_card)
        self.wind_icon.setAlignment(Qt.AlignCenter)
        self.wind_icon.setStyleSheet("font-size: 20px;")
        self.wind_val = QLabel("--", self.details_card)
        self.wind_val.setAlignment(Qt.AlignCenter)
        self.wind_val.setObjectName("detail_value")
        self.wind_lbl = QLabel("WIND", self.details_card)
        self.wind_lbl.setAlignment(Qt.AlignCenter)
        self.wind_lbl.setObjectName("detail_label")
        wind_layout.addWidget(self.wind_icon)
        wind_layout.addWidget(self.wind_val)
        wind_layout.addWidget(self.wind_lbl)
        
        details_layout.addLayout(feels_layout)
        details_layout.addLayout(humidity_layout)
        details_layout.addLayout(wind_layout)
        
        results_layout.addWidget(self.details_card)
        card_layout.addWidget(self.results_container)
        main_layout.addWidget(self.card)
        
        # Initialize opacity effect for animations
        self.opacity_effect = QGraphicsOpacityEffect(self.results_container)
        self.results_container.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0) # Initially hidden until a search
        
        # Apply CSS stylesheets
        self.update_background_gradient()
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_name.returnPressed.connect(self.get_weather)
        
    def update_background_gradient(self, weather_id=None):
        # Premium soft weather-themed gradients
        if weather_id is None:
            # Default soft sky blue
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a1c4fd, stop:1 #c2e9fb)"
        elif 200 <= weather_id <= 232: # Thunderstorm
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b6cb7, stop:1 #182848)"
        elif 300 <= weather_id <= 321 or 500 <= weather_id <= 531: # Rain
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3a7bd5, stop:1 #3a6073)"
        elif 600 <= weather_id <= 622: # Snow
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #83a4d4, stop:1 #b6fbff)"
        elif 701 <= weather_id <= 781: # Atmosphere/Fog
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #757f9a, stop:1 #d7dde8)"
        elif weather_id == 800: # Clear Sky (Sunrise Sunset Peach)
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fceade, stop:1 #f9a8d4)"
        elif 801 <= weather_id <= 804: # Clouds
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #cbd5e1, stop:1 #94a3b8)"
        else:
            gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a1c4fd, stop:1 #c2e9fb)"
            
        self.setStyleSheet(f"""
            QWidget#MainWindow {{
                background: {gradient};
            }}
            QFrame#glass_card {{
                background-color: rgba(255, 255, 255, 0.45);
                border: 1px solid rgba(255, 255, 255, 0.6);
                border-radius: 24px;
            }}
            QLabel#app_title {{
                font-family: 'Century Gothic', 'Montserrat', 'Segoe UI';
                font-size: 24px;
                font-weight: bold;
                color: #1e293b;
                margin-top: 10px;
                margin-bottom: 5px;
            }}
            QLineEdit#city_input {{
                background-color: rgba(255, 255, 255, 0.65);
                border: 1px solid rgba(0, 0, 0, 0.12);
                border-radius: 12px;
                color: #1e293b;
                font-family: 'Segoe UI';
                font-size: 15px;
                padding: 10px;
                qproperty-placeholderTextColor: rgba(30, 41, 59, 120);
            }}
            QLineEdit#city_input:focus {{
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #3b82f6;
            }}
            QPushButton#search_btn {{
                background-color: rgba(30, 41, 59, 0.08);
                border: 1px solid rgba(30, 41, 59, 0.18);
                border-radius: 12px;
                color: #1e293b;
                font-family: 'Segoe UI';
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
            }}
            QPushButton#search_btn:hover {{
                background-color: rgba(30, 41, 59, 0.15);
                border-color: rgba(30, 41, 59, 0.3);
            }}
            QPushButton#search_btn:pressed {{
                background-color: rgba(30, 41, 59, 0.04);
                border-color: rgba(30, 41, 59, 0.15);
            }}
            QLabel#emoji_label {{
                font-size: 76px;
                margin: 5px 0px;
            }}
            QLabel#temp_label {{
                font-family: 'Segoe UI', sans-serif;
                font-size: 54px;
                font-weight: 300;
                color: #1e293b;
            }}
            QLabel#desc_label {{
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: 500;
                color: #475569;
                text-transform: capitalize;
                margin-bottom: 5px;
            }}
            QFrame#details_card {{
                background-color: rgba(255, 255, 255, 0.35);
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 16px;
            }}
            QLabel#detail_value {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: #1e293b;
            }}
            QLabel#detail_label {{
                font-family: 'Segoe UI';
                font-size: 9px;
                font-weight: 600;
                color: #64748b;
            }}
        """)
        
    def fade_in_results(self):
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

    def get_weather(self):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            self.display_error("API Key Not Found")
            return
            
        city = self.city_name.text().strip()
        if not city:
            self.display_error("Enter City Name")
            return
            
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            error_messages = {
                400: "Invalid Request",
                401: "Invalid API Key",
                403: "Access Denied",
                404: "City Not Found",
                500: "Server Error",
                502: "Bad Gateway",
                503: "Service Unavailable",
                504: "Gateway Timeout"
            }
            status_code = response.status_code if 'response' in locals() else None
            msg = error_messages.get(status_code, f"HTTP Error ({status_code})")
            self.display_error(msg)
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error")
        except requests.exceptions.Timeout:
            self.display_error("Request Timeout")
        except Exception as e:
            self.display_error("Error Occurred")

    def display_error(self, message):
        self.temperature_label.setText("Error")
        self.emoji_label.setText("⚠️")
        self.description_label.setText(message)
        
        # Reset extra details
        self.feels_like_val.setText("--")
        self.humidity_val.setText("--")
        self.wind_val.setText("--")
        
        # Default gradient for errors
        self.update_background_gradient()
        self.fade_in_results()

    def display_weather(self, data):
        temp_c = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        self.temperature_label.setText(f"{temp_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        
        self.feels_like_val.setText(f"{feels_like:.0f}°C")
        self.humidity_val.setText(f"{humidity}%")
        self.wind_val.setText(f"{wind_speed:.1f} m/s")
        
        self.update_background_gradient(weather_id)
        self.fade_in_results()

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "❓"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())
