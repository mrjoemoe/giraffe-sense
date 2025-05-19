import time
from time_sync import update_time

def time_loop(interval=1):
    while True:
        update_time()
        time.sleep(interval)
