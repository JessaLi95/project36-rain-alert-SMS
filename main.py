import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from decouple import config

account_sid = "ACc107e0ac7ee9985e3cb27d60b694ff46"
auth_token = config('AUTH_TOKEN')
api_key = config('API_KEY')
end_point = "https://api.openweathermap.org/data/2.5/onecall?parameters"
parameters = {
    "lat": 53.68,
    "lon": -1.49,
    "exclude": "current,minutely,daily",
    "appid": api_key
}

response = requests.get(end_point, params=parameters)
response.raise_for_status()
hourly_weather = response.json()['hourly'][:12]

will_rain = False
for hour_data in hourly_weather:
    weather_id = hour_data['weather'][0]['id']
    if weather_id < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
                    .create(
                         body="It's going to rain today, remember to bring your 🌂",
                         from_="+16076009148",
                         to="+447536128991"
                     )
    print(message.status)