import paho.mqtt.client as mqtt
import json
from RelayCtrl import RelayCtrl


class MyMQTTClass(mqtt.Client):
    
    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        print('Type: {0} -> Content: {1}'.format(type(msg.payload), msg.payload))
        msg_info = json.loads(msg.payload)
        print('Type: {0} -> MSG INFO: {1}'.format(type(msg_info), msg_info))
        print('{0}'.format(json.dumps(msg_info, indent=4)))
        relay_topic = msg_info['relay_topic']
        relay_cmd = msg_info['relay_cmd']
        rc = RelayCtrl()
        rc_resp = rc.handle_cmd(relay_topic, relay_cmd)

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        server = '10.3.141.1'
        port = 1883
        topic = 'conquest/relay/command'
        qos = 0
        self.connect(server, port, 60)
        self.subscribe(topic, qos)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc

# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.


mqttc = MyMQTTClass('cq_relay_ctrl')
rc = mqttc.run()

