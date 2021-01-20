# Import Pin definition for esp8266
from machine import Pin
# Import time and machine libraries
import time
import machine

# ESP Pin for the relay
Rpin_main = Pin(1, Pin.OUT, value=0)  # Relay Pin
Rpin_entry = Pin(2, Pin.OUT, value=0)  # Relay Pin
Rpin_patio = Pin(3, Pin.OUT, value=0)  # Relay Pin

# Define di timeouts
timeouts = 2
# Define the topics


class RelayCtrl:

    def __init__(self, topic, loc, cmd):
        self.topic = topic
        self.loc = self
        self.cmd = cmd

    # Send relay status and turn it ON
    @staticmethod
    def _relay_action(r_pin, action):
        if action == "ON":
            r_pin.on()
        elif action == "OFF":
            r_pin.off()
        else:
            pass

        return r_pin.value()

    # Received messages from subscriptions will be delivered to this callback
    def handle_cmd(self):
        if self.topic == b"conquest/main/command":

            if self.cmd == b"Restart":
                relay_status = 2
                time.sleep(5)
                machine.reset()
            elif self.cmd == b"":
                relay_status = -1

        elif self.topic == b"conquest/relay/command":
                if self.loc == 'main':
                    r_pin = Rpin_main
                elif self.loc == 'entry':
                    r_pin == Rpin_entry
                elif self.loc == 'patio':
                    r_pin = Rpin_patio

                relay_status = self._relay_action(r_pin, self.cmd)

        else:
            relay_status = "CMD Invalid!"

        return relay_status
