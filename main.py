import sys, os, requests
from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QPushButton,QVBoxLayout,QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from dotenv import load_dotenv
load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter the City Name",self)
        self.city_name=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather",self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(700,300,500,500)
        self.setWindowIcon(QIcon("Weather_App/icon.jpg"))
        self.city_name.setPlaceholderText("City Name")
        self.temperature_label.setWordWrap(True)

        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_name.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_name.setObjectName("city_name")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel,QLineEdit,QPushButton{
                padding:20px;
            }
            QLabel#city_label{
                font-family:Algerian;
                font-size:40px;
            }
            QLineEdit#city_name{
                font-family:Courier new;
                font-size:25px;
                font-weight:bold;
            }
            QPushButton#get_weather_button{
                font-family:Gabriola;
                font-size:25px;
                font-weight:bold;
            }
            QLabel#temperature_label{
                font-family:calibri;
                font-size:75px;
            }
            QLabel#emoji_label{
                font-family:segoe UI emoji;
                font-size:100px;
            }
            QLabel#description_label{
                font-family:Goudy old style;
                font-size:30px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key=os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            self.display_error("API key not set. See README")
            return
        city=self.city_name.text().strip()
        if not city:
            self.display_error("Please enter a city name")
            return
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response=requests.get(url,timeout=10)
            response.raise_for_status()         #raise the exception if there is any HTTPError
            data=response.json()
            if data.get("cod")==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:   # requests method will return the status code of 400 to 500 is called HTTPError
            error_messages = {
                400: "Invalid request\nPlease check your input",
                401: "Unauthorized\nInvalid API key",
                403: "Forbidden\nAccess denied",
                404: "Not Found\nCity not found",
                500: "Internal Server Error\nPlease try again later",
                502: "Bad Gateway\nInvalid response from server",
                503: "Service unavailable\nServer is down",
                504: "Gateway timeout\nNo response from the server"
            }
            message = error_messages.get(response.status_code, f"HTTP Error occurred\n{http_error}")
            self.display_error(message)
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error - Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Request timeout")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")


    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;font-family:poor richard;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temp_c=data["main"]["temp"]
        weather_id=data["weather"][0]["id"]
        weather_description=data["weather"][0]["description"]

        self.temperature_label.setText(f"{temp_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod         #because it belongs to class but it didn't use any instance method
    def get_weather_emoji(weather_id):
        if weather_id >= 200 and weather_id <= 232:
            return "⛈️"
        elif 300<= weather_id <=321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <=622:
            return "❄️"
        elif 701 <= weather_id <=741:
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
            return ""

if __name__=="__main__":
    app=QApplication(sys.argv)
    weather=WeatherApp()
    weather.show()
    sys.exit(app.exec_())
