# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
#
import network
#import esp
import gc
import webrepl

gc.collect()
webrepl.start()

#esp.osdebug(None)

#
# Set up WLAN
#
ssid = 'conquest_oh'
password = '!c0nqu#st2252'
ip = '192.168.50.2'
net_mask = '255.255.255.0'
gateway = '192.168.50.1'
dns = '192.168.50.1'

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.ifconfig([ip, net_mask, gateway, dns])
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


do_connect()
