import pytuya
import config
import requests
from time import sleep
import sys
from logzero import logger


from dateutil import parser
from datetime import datetime, timedelta

d = pytuya.OutletDevice(config.DEVICE_ID, config.IP_ADDRESS, config.LOCAL_KEY)
data = d.status()
logger.info('Dictionary %r' % data)
logger.info('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device


def get_status():
    logger.info("Getting Status")
    try:
        return requests.get(f'http://{config.MAD_IP}:{config.MAD_PORT}/get_status', auth=(config.MAD_USERNAME, config.MAD_PASSWORD)).json()
    except requests.exceptions.Timeout: 
        logger.error('Connection to get_status timed-out')
    except requests.exceptions.RequestException as e:
        logger.error(str(e))
    except Exception as e:
        logger.error("General error {0}".format(e))

def toggle():
    # Toggle switch state
    logger.info("Toggling state of switch")
    data = d.set_status(not switch_state)  # This requires a valid key
    switch_state = data['dps']['1']

    if data:
        logger.info('set_status() result %r' % data)
    data = d.set_timer(4)  # This requires a valid key

    if data:
        logger.info('set_status() result %r' % data)
    data = d.status()
    logger.info('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device

def parse_status(device_status_response):
    table_header = ['Origin', 'Route', 'Pos', 'Last Data']
    table_contents = []
    for device in device_status_response:
        try:
            if config.MAD_DEVICE_FILTER in device['name']:
                logger.info("Found device with name: " + device['name'])
                parsed_device_last_proto_datetime = datetime.fromtimestamp(device.get('lastProtoDateTime'))
                logger.info("Got Datetime " + parsed_device_last_proto_datetime.strftime("%m/%d/%Y, %H:%M:%S"))
                latest_acceptable_datetime = (datetime.now() - timedelta(minutes=config.ALERT_TIME_MINUTES))
                formatted_device_last_proto_time = parsed_device_last_proto_datetime.strftime("%H:%M")
                print(device['name'] + formatted_device_last_proto_time)
                if parsed_device_last_proto_datetime < latest_acceptable_datetime:
                    print("Toggle")
                    toggle()
                    sleep(60)
                    break
        except Exception as e:
            logger.error(e)
            formatted_device_last_proto_time = 'Unknown'



def main():
    """ Main entry point of the app """
    print("Starting Monitoring")
    while True:
        a = get_status()
        parse_status(a)
        sleep(120)



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()