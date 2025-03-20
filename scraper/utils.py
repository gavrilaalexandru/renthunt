import time
import random
import os
import csv
from datetime import datetime


def create_dirs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    os.makedirs(os.path.join(root_dir, "Data"), exist_ok=True)


def random_delay(min_seconds=1, max_seconds=3):
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def save_to_csv(data, filename):
    if not data:
        print("No data found")
        return

    fieldnames = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        w = csv.DictWriter(csvfile, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data)


def generate_timestamp():
    return datetime.now().strftime("%d%m%Y_%H%M%S")
