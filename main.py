# 3rd party
import os
import _thread
import time


# internal
from led_driver import signals_loop, blink_loop
from giraffe_net import configure_network, wifi_scan_loop


SIGNALS_FOLDER = "signals"
INTERVAL_S = 3



def initialize(folder="signals"):
    """ Set up device folders
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

initialize(folder=SIGNALS_FOLDER)
configure_network()
_thread.start_new_thread(wifi_scan_loop, (SIGNALS_FOLDER, INTERVAL_S))
_thread.start_new_thread(signals_loop, (INTERVAL_S,))
blink_loop()
