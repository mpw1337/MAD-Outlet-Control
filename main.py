import pytuya
import config

d = pytuya.OutletDevice(config.DEVICE_ID, config.IP_ADDRESS, config.LOCAL_KEY)
data = d.status()
print('Dictionary %r' % data)

print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device

# Toggle switch state
switch_state = data['dps']['1']
data = d.set_status(not switch_state)  # This requires a valid key

if data:
    print('set_status() result %r' % data)
data = d.set_timer(4)  # This requires a valid key

if data:
    print('set_status() result %r' % data)
data = d.status()
print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device