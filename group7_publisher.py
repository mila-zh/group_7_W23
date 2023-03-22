import random

import paho.mqtt.client as mqtt
import time
import json
import sys
from group7_generator import DataGenerator



if len(sys.argv) < 3:
    print("Please provide a device ID and location as arguments.")
    sys.exit(1)

device_id = sys.argv[1]
location = sys.argv[2]
min_temperature = 20
max_temperature = 30

broker = "localhost"
port = 1883
topic = "your/topic"

data_generator = DataGenerator(device_id, min_temperature, max_temperature, location=location)

client = mqtt.Client(f"Publisher_{device_id}")
client.connect(broker, port)

# skipping blocks of transmissions

skip_transmission_probability = 0.05  # Adj# ust this value as needed
skip_transmission_count = 5  # Adjust this value as needed

while True:

    data = data_generator.generate_data()

    # Simulate skipping blocks of transmissions
    if random.random() < skip_transmission_probability:
        print("Skipping a block of transmissions")
        time.sleep(skip_transmission_count)
        continue

    # Your transmission will fail with a frequency of about 1 in very 100 transmissions. This must not be deterministic!
    # random.random() < 0.01 have probability of almost 1/100
    if random.random() < 0.01:
        print("Transmission failed")
    else:
        client.publish(topic, json.dumps(data))
        print(f"Sending message: {json.dumps(data)}")

    time.sleep(1)
