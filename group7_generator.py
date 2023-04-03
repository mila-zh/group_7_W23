import random
import time


class DataGenerator:

    # Constructor of DataGenerator class
    # device_id: a unique identifier for the device
    # min_value: minimum value for the generated data
    # max_value: maximum value for the generated data
    # wild_value_factor: the factor by which a wild data value will be multiplied
    # wild_value_chance: the probability that a wild data value happens
    # location: location information for the device
    def __init__(self, device_id, min_value, max_value, wild_value_factor=10, wild_value_chance=0.1, location=None):
        self.device_id = device_id
        self.min_value = min_value
        self.max_value = max_value
        self.wild_value_factor = wild_value_factor
        self.wild_value_chance = wild_value_chance
        self.location = location

# generate_data method
    def generate_data(self):

        # Generate a random value that in 1 decimal from min_value to max_value
        value = round(random.uniform(self.min_value, self.max_value), 1)

        # Create "wild data" if random.random() is smaller than wild_value_chance(default: 0.1)
        if random.random() < self.wild_value_chance:
            value = 10

        # Generate the time stamp in the form of '%Y-%m-%d %H:%M:%S'
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        # Create a dictionary containing all information
        data = {"device_id": self.device_id, "value": value, "timestamp": timestamp, "location": self.location}

        return data
