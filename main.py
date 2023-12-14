import requests
import os
import time
import pytz
from datetime import datetime 

threshold = float(os.getenv("THRESHOLD"))
auth = str(os.getenv("AUTH"))
dest_url = str(os.getenv("DEST_URL"))

source_url = "https://www.ag.ch/app/hydrometrie/kiwis/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&metadata=true&format=json&ts_id=26780042"
intervall = 60
old_time = ""
alarm = False


def get_station(url: str):
    try:
        content = requests.get(url)
    except ConnectionError:
        print("Webseite nicht erreicht.")
        return {"name": "ConnectionError", "timestamp": datetime.now(), "value": "0"}
    station_name = content.json()[0]['station_name']
    station_unit = content.json()[0]['ts_unitsymbol']
    station_timestamp = datetime.strptime(content.json()[0]['data'][0][0],"%Y-%m-%dT%H:%M:%S.%f%z")
    station_value = content.json()[0]['data'][0][1]
    return {"name": station_name, "timestamp": station_timestamp.strftime("%d.%m.%Y %H:%M"), "value": station_value, "unit": station_unit}



# Senden des Alarms an Server via HTTP POST Request
def send_alarm(station: dict, url: str, auth: str):
    now = datetime.now(pytz.timezone("Europe/Zurich"))
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    request_data = { 
		'type': "ALARM",
		'timestamp': timestamp,
		'sender': "Abflussalarm",
		'authorization': auth,
		'data': { 
            "keyword": "Hochwasser Suhre",
			'message': [
				"Schwellwert der Suhre wurde überschritten"
			],
            "units": [
                {
                    "address":"suhre"
                }
            ],
        'custom': {
            'water_station': station["name"],
            'water_ts': station["timestamp"],
            'water_unit': station["unit"],
            'water_abfluss': station["value"]
        }
		}
	}
	#Senden Request an FE2 Server
    r = requests.post(url, json = request_data)
    return r


while True:
    now = datetime.now()
    now_datetime = str(now.strftime("%d.%m.%Y %H:%M"))
    if now.minute == 5 or now.minute == 15 or now.minute == 25 or now.minute == 35 or now.minute == 45 or now.minute == 55:
        station = get_station(source_url)
        now_time = station["timestamp"]
        now_value = float(station["value"])
        if now_time != old_time:
            old_time = now_time
            if not alarm and now_value > threshold:
                print(now_datetime + ": ALARM!!!")
                send_alarm(station, dest_url, auth)
                alarm = True
            elif alarm and now_value < threshold:
                print(now_datetime + ": Alarm Ende")
                alarm = False

            print(now_datetime + ": " + station["name"] + " from " + station["timestamp"] + " : " + str(station["value"]) + station["unit"])
        else:
            print(now_datetime + ": No new data")
    # else:
    #     print(now.minute)
    time.sleep(intervall)
