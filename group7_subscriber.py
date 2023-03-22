import paho.mqtt.client as mqtt
import json
import sys
from tkinter import *


def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())

    # Transmit “wild data” something that is completely off the chart. Again your subscriber should be able to handle this
    # Handle out-of-range data
    if data["value"] < min_temperature or data["value"] > max_temperature:
        print("Out-of-range data received:", data)
    else:
        print("Data received:", data)

        # Update the tkinter label with received data
        data_label.config(text=f"{data['device_id']} - {data['value']} - {data['timestamp']}")

        root.after_cancel(timeout_id)  # Cancel the timeout


def on_timeout():
    data_label.config(text="Data missing", fg="red")


if len(sys.argv) < 2:
    print("Please provide a location as an argument.")
    sys.exit(1)

device_id = sys.argv[0]
location = sys.argv[1]
min_temperature = 20
max_temperature = 30

broker = "localhost"
port = 1883
topic = "your/topic"

client = mqtt.Client(f"Subscriber_{location}")
client.connect(broker, port)
client.subscribe(topic)
client.on_message = on_message

# Tkinter application
root = Tk()
root.title(f"Temperature Monitor - {location}")

data_label = Label(root, text="Waiting for data...", font=("Helvetica", 18))
data_label.pack(padx=10, pady=10)

timeout_id = root.after(5000, on_timeout)  # Set a timeout of 5 seconds

client.loop_start()  # Start the MQTT loop in a separate thread

root.mainloop()  # Run the Tkinter main loop

client.loop_stop()  # Stop the MQTT loop when the Tkinter main loop ends
