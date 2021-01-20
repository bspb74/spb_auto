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
ssid = 'neverNeverLand'
password = 'p3terp@n'
ip = '172.16.1.20'
net_mask = '255.255.255.0'
gateway = '172.16.1.1'
dns = '172.16.1.1'


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
