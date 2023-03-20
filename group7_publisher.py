import paho.mqtt.client as mqtt
import group7_generator
import time
import json

# connect broker
mqtt_broker = "mqtt.eclipseprojects.io"

# client
client = mqtt.Client("Audio_SineWave")

# connect client to broker
client.connect(mqtt_broker)