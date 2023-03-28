import random

import paho.mqtt.client as mqtt
import time
import json
import sys
from group7_generator import DataGenerator


# Check that device ID and location have been provided as command-line arguments
if len(sys.argv) < 3:
    print("Please provide a device ID and location as arguments.")
    sys.exit(1)

# assign the input device id and location to parameter
device_id = sys.argv[1]
location = sys.argv[2]

# Set the range of temperatures that the data generator will produce
min_temperature = 20
max_temperature = 30

# Set up the MQTT broker and topic that messages will be published to
broker = "localhost"
port = 1883
topic = "location temperature"

# Create a data generator instance for this device
data_generator = DataGenerator(device_id, min_temperature, max_temperature, location=location)

# Set up the MQTT client instance for publishing messages
client = mqtt.Client(f"Publisher_{device_id}")
client.connect(broker, port)

# skipping blocks of transmissions

skip_transmission_probability = 0.05  # The possible that "Skip transmission" happens
skip_transmission_count = 5  # Time in seconds when "Skip transmission" happens


# Enter an infinite loop that publishes data to the MQTT broker
while True:

    data = data_generator.generate_data()

    # Simulate skipping blocks of transmissions
    if random.random() < skip_transmission_probability:
        print("Skipping a block of transmissions")
        time.sleep(skip_transmission_count)
        continue

    # Simulate transmission failures with a probability of about 1 in 100
    if random.random() < 0.01:
        print("Transmission failed")
    else:
        # Publish the message to the MQTT broker as a JSON-encoded string
        client.publish(topic, json.dumps(data))
        print(f"Sending message: {json.dumps(data)}")

    # Wait for 1 second before publishing the next message
    time.sleep(1)
