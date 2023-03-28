import paho.mqtt.client as mqtt
import json
import sys
from tkinter import *


# The callback function that will be called when a message is received
def on_message(client, userdata, message):
    # Decode the incoming message and parse the data as a JSON object
    data = json.loads(message.payload.decode())

    # Ignore the data if the location doesn't match
    if data.get("location") != location:
        return

    # Handle out-of-range data
    if data["value"] < min_temperature or data["value"] > max_temperature:
        print("Out-of-range data received:", data)
        # Update the UI to display the out-of-range data in red
        data_label.config(text=f"Out-of-range data: {data['device_id']} - {data['value']} - {data['timestamp']} - "
                               f"{data['location']}",
                          fg="red")
    else:
        print("Data received:", data)
        # Update the UI to display the received data in black
        data_label.config(text=f"{data['device_id']} - {data['value']} - {data['timestamp']} - {data['location']}",
                          fg="black")

    # Cancel the timeout after data is received
    root.after_cancel(timeout_id)


# Set text to red and show "Data missing" in the UI
def on_timeout():
    data_label.config(text="Data missing", fg="red")


# Check for the required command line arguments
if len(sys.argv) < 2:
    print("Please provide a location as an argument.")
    sys.exit(1)

# Set the location argument
location = sys.argv[1]

# Set temperature range
min_temperature = 20
max_temperature = 30

# Set MQTT broker settings
broker = "localhost"
port = 1883
topic = "location temperature"

# Create an MQTT client instance and configure the message callback
client = mqtt.Client(f"Subscriber_{location}")
client.connect(broker, port)
client.subscribe(topic)
client.on_message = on_message

# Initialize the Tkinter application
root = Tk()
root.title(f"Temperature Monitor - {location}")


# Create a label to display data
data_label = Label(root, text="Waiting for data...", font=("Helvetica", 18))
data_label.pack(padx=10, pady=10)

timeout_id = root.after(5000, on_timeout)  # Set a timeout of 5 seconds

client.loop_start()  # Start the MQTT loop in a separate thread

root.mainloop()  # Run the Tkinter main loop

client.loop_stop()  # Stop the MQTT loop when the Tkinter main loop ends
