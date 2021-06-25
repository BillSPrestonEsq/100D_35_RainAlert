import requests
import os
from twilio.rest import Client

API_TEMPLATE = "https://api.openweathermap.org/data/2.5/onecall"
EXCLUDE = "current,minutely,daily"

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
my_phone = os.getenv('MY_PHONE')
twilio_phone = os.environ.get('TWILIO_PHONE')
owm_api_key = os.environ.get('OWM_API_KEY')
latitude = os.environ.get('LATITUDE')
longitude = os.environ.get('LONGITUDE')

weather_parameters = {
    "lat":latitude,
    "lon":longitude,
    "appid":owm_api_key,
    "exclude":EXCLUDE,
}

response = requests.get(API_TEMPLATE,params=weather_parameters)
response.raise_for_status()
weather_data = response.json()["hourly"]
bring_umbrella = False
hour_num = 0

for hour in weather_data[:12]:
    for condition in hour["weather"]:
        if condition["id"] < 700:
            bring_umbrella = True

if bring_umbrella == True:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☂️",
        from=twilio_phone,
        to=my_phone
    )
    print(message.status)
