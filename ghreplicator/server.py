import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('#')


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def main():
    # Create a websockets client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the firehose
    client.connect('firehose.openstack.org')
    # Listen forever
    client.loop_forever()
