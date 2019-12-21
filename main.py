import pytuya
import config
import requests
from time import sleep
import sys


from dateutil import parser
from datetime import datetime, timedelta

d = pytuya.OutletDevice(config.DEVICE_ID, config.IP_ADDRESS, config.LOCAL_KEY)
data = d.status()
print('Dictionary %r' % data)
print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device


def get_status():
    try:
        return requests.get(f'http://{config.MAD_IP}:{config.MAD_PORT}/get_status', auth=(config.MAD_USERNAME, config.MAD_PASSWORD)).json()
    except requests.exceptions.Timeout: 
        print('Connection to get_status timed-out')
    except requests.exceptions.RequestException as e:
        print(str(e))
    except Exception as e:
        print("General error {0}".format(e))

def toggle():
    # Toggle switch state
    print("Toggling state of switch")
    data = d.set_status(not switch_state)  # This requires a valid key
    switch_state = data['dps']['1']

    if data:
        print('set_status() result %r' % data)
    data = d.set_timer(4)  # This requires a valid key

    if data:
        print('set_status() result %r' % data)
    data = d.status()
    print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device

def parse_status(device_status_response):
    table_header = ['Origin', 'Route', 'Pos', 'Last Data']
    table_contents = []
    for device in device_status_response:
        try:
            if config.MAD_DEVICE_FILTER in device['origin']:
                datetime_from_status_json = parser.parse(device['lastProtoDateTime'])
                latest_acceptable_datetime = (datetime.now() - timedelta(minutes=config.ALERT_TIME_MINUTES))
                formatted_device_last_proto_time = datetime_from_status_json.strftime("%H:%M")
                print(device['origin'] + formatted_device_last_proto_time)
                if datetime_from_status_json < latest_acceptable_datetime:
                    print("Toggle")
                    toggle()
                    sleep(60)
                    break
        except Exception:
            formatted_device_last_proto_time = 'Unknown'
while True:
    a = get_status()
    parse_status(a)
    sleep(120)