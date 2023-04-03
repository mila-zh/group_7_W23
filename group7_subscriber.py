import paho.mqtt.client as mqtt
import json
import sys
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from time import sleep
import queue
import threading
import time





class MatplotlibPlot:
    def __init__(
            self, master, datas: list[dict], update_interval_ms: int = 200, padding: int = 5,
            fig_config: callable = None, axes_config: callable = None
    ):
       

        # Creates the figure
        fig = plt.Figure()
        # Calls the config function if passed
        if fig_config:
            fig_config(fig)

        # Creates Tk a canvas
        canvas = FigureCanvasTkAgg(figure=fig, master=master)
        # Allocates the canvas
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True, padx=padding, pady=padding)

        # Creates an axes
        axes = fig.add_subplot(1, 1, 1)

        # For each data entry populate the axes with the initial data values. Also, configures the lines with the
        # extra key-word arguments.
        for data in datas:
            axes.plot(data["x"], data["y"])
            _kwargs = data.copy()
            _kwargs.pop("x")
            _kwargs.pop("y")
            axes.lines[-1].set(**_kwargs)

        # Calls the config function if passed
        if axes_config:
            axes_config(axes)

        # Creates a function animation which calls self.update_plot function.
        self.animation = animation.FuncAnimation(
            fig=fig,
            func=self.update_plot,
            fargs=(canvas, axes, datas),
            interval=update_interval_ms,
            repeat=False,
            blit=True
        )

    # noinspection PyMethodMayBeStatic
    def update_plot(self, _, canvas, axes, datas):
        # Variables used to update xx and yy axes limits.
        update_canvas = False
        xx_max, xx_min = axes.get_xlim()
        yy_max, yy_min = axes.get_ylim()

        # For each data entry update its correspondent axes line
        for line, data in zip(axes.lines, datas):
            line.set_data(data["x"], data["y"])
            _kwargs = data.copy()
            _kwargs.pop("x")
            _kwargs.pop("y")
            line.set(**_kwargs)

            # If there are more than two points in the data then update xx and yy limits.
            if len(data["x"]) > 1:
                if min(data["x"]) < xx_min:
                    xx_min = min(data["x"])
                    update_canvas = True
                if max(data["x"]) > xx_max:
                    xx_max = max(data["x"])
                    update_canvas = True
                if min(data["y"]) < yy_min:
                    yy_min = min(data["y"])
                    update_canvas = True
                if max(data["y"]) > yy_max:
                    yy_max = max(data["y"])
                    update_canvas = True

        # If limits need to be updates redraw canvas
        if update_canvas:
            axes.set_xlim(xx_min, xx_max)
            axes.set_ylim(yy_min, yy_max)
            canvas.draw()

        # return the lines
        return axes.lines


class CustomScaler:
    
    def __init__(self, master, init: int = None, start: int = 0, stop: int = 100,
                 padding: int = 5, callback: callable = None):

        self.start = start
        self.stop = stop

        if init:
            self.value = IntVar(master=master, value=init, name="scaler_value")
        else:
            self.value = IntVar(master=master, value=(self.stop - self.start) // 2, name="scaler_value")

        if callback:
            self.value.trace_add("write", callback=callback)


        #Button(master=master, text="Random Begin", command=self.foo, repeatdelay=10, repeatinterval=100) \
           # .pack(side=LEFT, fill=Y, padx=padding, pady=padding)
        Button(master=master, text="Go", command=self.t1) \
               .pack(side=LEFT, fill=Y, padx=padding, pady=padding)     


    def randomSet(self):
        _value = self.value.get()
        #data = json.loads(message.payload.decode())
        self.value.set(Tem)
       
    
    def print_hello(self):
        while 1:
            time.sleep(1)
            self.randomSet()
   
    def t1(self):
        t1= threading.Thread(target=self.print_hello)
        t1.start()
        

       
def scaler_changed(my_vars: list[dict], scaler: CustomScaler) -> None:
    my_vars[0]["x"].append(len(my_vars[0]["x"]))
    my_vars[0]["y"].append(scaler.value.get())


def my_axes_config(axes: plt.Axes) -> None:
    axes.set_xlabel("Time Pass (Second)")
    axes.set_ylabel("Temperature")
    #axes.set_title("Temperature Wave")






# The callback function that will be called when a message is received
def on_message(client, userdata, message):
    # Decode the incoming message and parse the data as a JSON object
    data = json.loads(message.payload.decode())
    global Tem
    Tem = int(data['value'])
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
# Create a window to display figure
frame_scaler = Frame(master=root)

scaler = CustomScaler(
master=frame_scaler, start=0, stop=100, callback=lambda n, i, m: scaler_changed(my_vars, scaler)
)
frame_scaler.pack(padx=10, pady=30)
frame_plot = Frame(master=root)
my_vars = [{"x": [], "y": []}, ]

MatplotlibPlot(master=frame_plot, datas=my_vars, axes_config=my_axes_config, update_interval_ms=10)
frame_plot.pack(padx=10, pady=40)
root.mainloop()  # Run the Tkinter main loop

client.loop_stop()  # Stop the MQTT loop when the Tkinter main loop ends
