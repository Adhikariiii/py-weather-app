from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import sys
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.text_label = QLabel("Enter the name of city: ", self)
        self.input_label = QLineEdit(self)
        self.search_btn = QPushButton("Get Weather")
        self.city_name = QLabel( self)
        self.temprature = QLabel()
        self.wind_spped = QLabel()
        self.description = QLabel()
        self.emoji = QLabel()
        self.initUI()

    def initUI(self):
        self.city_name.setObjectName("city")
        self.temprature.setObjectName("temprature")
        self.wind_spped.setObjectName("wind_spped")
        self.description.setObjectName("description")
        self.input_label.setObjectName("input")
        self.emoji.setObjectName("emoji")
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

        vbox = QVBoxLayout()
       
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.temprature)
        vbox.addWidget(self.wind_spped)
        vbox.addWidget(self.description)
        vbox.addWidget(self.text_label)
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.search_btn)
        vbox.addWidget(self.emoji)

        self.setLayout(vbox)
        self.city_name.setAlignment(Qt.AlignCenter)
        self.temprature.setAlignment(Qt.AlignCenter)
        self.wind_spped.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.text_label)
        hbox.addWidget(self.input_label)
        hbox.addWidget(self.search_btn)

        vbox.addLayout(hbox)



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
            print(data)
            self.display_weather(data)
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

     

    
    def display_weather(self, data):
        city = data['name']
        temprature = data['main']['temp']
        temp_in_celcius = temprature -  273.15
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        weather_id = data['weather'][0]['id']
        
        
        self.city_name.setText(city)
        self.temprature.setText(str(f"{temp_in_celcius:.0f}℃"))
        self.wind_spped.setText(f"Wind Speed: {str(wind_speed)}")
        self.description.setText(f"Description: {str(description)}")
        self.emoji.setText(self.display_emoji(weather_id))
        self.input_label.clear()
    
    def display_error(self, message):
        self.city_name.setText(message)
        self.temprature.clear()
        self.wind_spped.clear()
        self.description.clear()
        self.input_label.clear()
        self.emoji.clear()

    @staticmethod
    def display_emoji(weather_id):
        if weather_id >=200 and weather_id <= 232:
            return "⛈️"
        elif weather_id >=300 and weather_id <= 321:
            return "🌦️"
        elif weather_id >=500 and weather_id <= 531:
            return "🌧️"
        elif weather_id >=600 and weather_id <= 622:
            return "🌨️"
        elif weather_id >=701 and weather_id <= 781:
            return "🌪️"
        elif weather_id ==800 :
            return "☀️"
        elif weather_id >=800 and weather_id <=804 :
            return "☁️"
            


def main():
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


