# 3rd party
import os
import _thread
import time


# internal
from led_driver import led_loop, blink_loop
from giraffe_net import configure_network, scan_loop
from pubsub import EventBus

SIGNALS_FOLDER = "signals"
INTERVAL_S = 8



def device_setup(folder="signals"):
    """ Set up device folders.
    currently just 1 folder for devices called 'signals' to track device signal strength
    """
    def _delete_folder_recursive(path):
        for entry in os.listdir(path):
            full_path = path + "/" + entry
            try:
                os.remove(full_path)
            except OSError:
                delete_folder_recursive(full_path)
        os.rmdir(path)

    # Reset signal folder
    try:
        _delete_folder_recursive(folder)
    except OSError:
        pass  # Folder doesn't exist yet — that's fine

    os.mkdir(folder)


# create folders
device_setup(folder=SIGNALS_FOLDER)

# setup device network
configure_network()

# start wifi scan loop - this loop measure signal strength of other devices
# dumps data to file
_thread.start_new_thread(scan_loop, (SIGNALS_FOLDER, INTERVAL_S - 1))


bus = EventBus()


# loop to read from files - append data to queues
_thread.start_new_thread(led_loop, (bus, INTERVAL_S))

def test_update(rssi):
    print("Received new test update:", rssi)

bus.subscribe("test_update", test_update)

# main loop to pulse the LED
blink_loop()



