import random
import time


class DataGenerator:

    def __init__(self, device_id, min_value, max_value, wild_value_factor=10, wild_value_chance=0.01, location=None):
        self.device_id = device_id
        self.min_value = min_value
        self.max_value = max_value
        self.wild_value_factor = wild_value_factor
        self.wild_value_chance = wild_value_chance
        self.location = location

    def generate_data(self):
        value = round(random.uniform(self.min_value, self.max_value), 1)

        if random.random() < self.wild_value_chance:
            value *= self.wild_value_factor

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        data = {"device_id": self.device_id, "value": value, "timestamp": timestamp}

        if self.location:
            data["location"] = self.location

        return data
