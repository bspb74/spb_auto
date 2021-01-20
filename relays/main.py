from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import time

# Initialize PINs to control relays
main_pin = Pin(5, Pin.OUT)
entry_pin = Pin(4, Pin.OUT)
patio_pin = Pin(0, Pin.OUT)
awning_pin = Pin(3, Pin.OUT)
# Initialize to READ relay PINs
main_button_pin = Pin(12, Pin.IN)  # D8
# entry_button_pin = Pin(2, Pin.IN)  # D5
patio_button_pin = Pin(13, Pin.IN)  # D6
awning_button_pin = Pin(15, Pin.IN)  # D7


# Default MQTT server to connect to
SERVER = "192.168.50.1"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
S_TOPIC = "conquest/lights/command/#"
P_TOPIC = "conquest/lights/status"
BUTTON_P_TOPIC = "conquest/lights/command"

rpin_state_pub = 0
sub_topic = str()
pin_state = str()
button_pin = None
tgl_pin = None
button_state = 0
s_topic = None


def hndl_button_main(pin):
    global tgl_pin
    global button_pin
    global s_topic
    tgl_pin = main_pin
    button_pin = main_button_pin
    s_topic = 'main'


def hndl_button_entry(pin):
    global tgl_pin
    global button_pin
    global s_topic
    tgl_pin = entry_pin
    button_pin = entry_button_pin
    s_topic = 'entry'


def hndl_button_patio(pin):
    global tgl_pin
    global button_pin
    global s_topic
    tgl_pin = patio_pin
    button_pin = patio_button_pin
    s_topic = 'patio'


def hndl_button_awning(pin):
    global tgl_pin
    global button_pin
    global s_topic
    tgl_pin = awning_pin
    button_pin = awning_button_pin
    s_topic = 'awning'


main_button_pin.irq(trigger=Pin.IRQ_RISING, handler=hndl_button_main)
# entry_button_pin.irq(trigger=Pin.IRQ_RISING, handler=hndl_button_entry)
patio_button_pin.irq(trigger=Pin.IRQ_RISING, handler=hndl_button_patio)
awning_button_pin.irq(trigger=Pin.IRQ_RISING, handler=hndl_button_awning)


def toggle_pin(t_pin):

    if t_pin.value():
        return "OFF"
    else:
        return "ON"


def c_pin_state(rpin, pin_state):
    # print('\n# PIN State from Topic: {0}'.format(pin_state))
    if pin_state == "ON":
        rpin.on()
    elif pin_state == "OFF":
        rpin.off()

    # print('{0} -> {1}'.format(rpin, rpin.value()))

    return rpin.value()


def sub_cb(topic, msg):
    global rpin_state_pub
    global sub_topic
    global pin_state
    print((topic, msg))
    sub_topic_tmp = str(topic).strip("'")
    sub_topic = str(sub_topic_tmp).split('/')[-1]
    print('Sub Topic: {0}'.format(sub_topic))
    pin_state_tmp = str(msg)
    pin_state = pin_state_tmp.split("'")[1]
    print('Location: {0} -> State: {1}'.format(sub_topic, pin_state))
    if sub_topic == 'main':
        rpin = main_pin
    elif sub_topic == 'entry':
        rpin = entry_pin
    elif sub_topic == 'patio':
        rpin = patio_pin
    elif sub_topic == 'awning':
        rpin = awning_pin
    elif sub_topic == 'reset':
        if pin_state == '1':
            machine.reset()

    if sub_topic:
        rpin_state = c_pin_state(rpin, pin_state)

        if not rpin_state:
            rpin_state_pub = "OFF"
        else:
            rpin_state_pub = "ON"


def main(server=SERVER):
    global tgl_pin, button_pin, button_state, s_topic
    debug = False
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(S_TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, S_TOPIC))

    try:
        while True:
            if s_topic is not None:
                print('{0}'.format(s_topic))
                trigger_cnt = 0
                for i in range(1, 10):
                    print('trigger count: {0}: button value: {1}'.format(str(trigger_cnt), str(button_pin.value())))
                    if button_pin.value() == 1:
                        print(trigger_cnt)
                        trigger_cnt += 1
                if trigger_cnt >= 7:
                    button_state = toggle_pin(tgl_pin)
                    if debug:
                        print('Button Toggle: {0}/{1}'.format(P_TOPIC, s_topic))
                    c.publish('{0}/{1}'.format(BUTTON_P_TOPIC, s_topic), button_state)
                    c.publish('{0}/{1}'.format(P_TOPIC, s_topic), button_state)
            msg_chk = c.check_msg()
            if msg_chk:
                c.publish('{0}/{1}'.format(P_TOPIC, sub_topic), rpin_state_pub)
            s_topic = None
    finally:
        c.disconnect()


main()
