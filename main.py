import requests
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt
import sys

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

        self.text_label = QLabel("Enter the name of the city: ")
        self.input_label = QLineEdit()
        self.search_btn = QPushButton("Search..")
        self.city_name = QLabel()
        self.temprature = QLabel()
        # self.emoji = QLabel()
        self.description = QLabel()
        self.wind_speed = QLabel()

        self.initUI()


    
    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.text_label)
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.search_btn)
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.temprature)
        # vbox.addWidget(self.emoji)
        vbox.addWidget(self.description)
        vbox.addWidget(self.wind_speed)

        self.setLayout(vbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.text_label)
        hbox.addWidget(self.input_label)
        hbox.addWidget(self.search_btn)
        vbox.addLayout(hbox)
        self.city_name.setObjectName("city")
        self.temprature.setObjectName("temprature")
        self.text_label.setObjectName("text_label")
        # self.emoji.setObjectName("emoji")
        self.input_label.setObjectName("input")
        self.setStyleSheet("""
               
                WeatherApp {
                    background: qlineargradient(
                        x1:0, y1:0,
                        x2:1, y2:1,
                        stop:0 #9fd3ff,
                        stop:0.35 #f6b1d0,
                        stop:0.65 #ffb48a,
                        stop:1 #fff1b6
                    );
                }

               
                QLabel {
                    background: transparent;
                    font-size: 40px;
                    color: #2b2b2b;
                }

                QLabel#text_label {
                    background: transparent;
                    font-size: 40px;
                }
                QLabel#city {
                    background: transparent;
                    font-size: 80px;
                    font-weight: bold;
                }

                QLineEdit#input {
                    padding: 12px;
                    min-width: 280px;
                    min-height: 48px;
                    font-size: 40px bold;
                    border-radius: 14px;
                    background: rgba(255, 255, 255, 0.85);
                    border: none;
                }

                QPushButton {
                    padding: 10px 18px;
                    font-size: 18px;
                    border-radius: 14px;
                    color: white;
                    background: #ff8fab;
                }

                QPushButton:hover {
                    background: #ff7096;
                }
                QLineEdit{
                           color:black;}
                """)


        self.city_name.setAlignment(Qt.AlignCenter)
        self.temprature.setAlignment(Qt.AlignCenter)
        # self.emoji.setAlignment(Qt.AlignCenter)
        self.wind_speed.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.search_btn.clicked.connect(self.get_weather)
    
    def get_weather(self):
     try:
        api_key = "2cad64a3367576ab6caa382874e179ef"
        city_name = self.input_label.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['cod'] == 200:
            self.display_weather(data)
            # print(data)
     except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                self.display_error("Bad reqeust")
            case 401:
                self.display_error("Unauthorized")
            case 403:
                self.display_error("Forbidden")
            case 404:
                self.display_error("Not Found")
            case 400:
                self.display_error("Bad reqeust")
            case 408:
                self.display_error("Request Timeout")
            case 429:
                self.display_error("Too many requests")
            case 500:
                self.display_error("Internal Server Error")
            case 502:
                self.display_error("Bad Gateway")
            case 503:
                self.display_error("Service unavailable")
            case 504:
                self.display_error("Gateway Timeout")
            case _: 
                self.display_error(f"Unexpcted Error: {http_error }")

     except requests.exceptions.ConnectionError:
         self.display_error("Connection Error!")

    def display_error(self, messaage):
        self.city_name.setText(messaage)
        self.temprature.clear()
        self.wind_speed.clear()
        self.description.clear()
        self.input_label.clear()


    def display_weather(self, data):
            temprature = data["main"]["temp"]
            city = data["name"]
            description = data["weather"][0]["description"]
            wind_speed = data['wind']['speed']
            temprature_celcius = temprature  - 273.15
            self.temprature.setText(f"{temprature_celcius:.0f}°C")
            self.city_name.setText(city)
            self.description.setText(description)
            self.wind_speed.setText(str(f"Wind Speed: {wind_speed}"))
            self.input_label.clear()
def main():
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
    