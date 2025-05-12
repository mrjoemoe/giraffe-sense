import network
import time
import urandom
import os


HEX_CHARS = "0123456789abcdef"
NETWORK_PREFIX = "giraffenet-"

def _get_or_create_short_uuid(path="uuid.txt"):
    """ Create unique ID and store for persistence
    """

    try:
        with open(path, "r") as f:
            return f.read().strip()
    except OSError:
        uuid = "".join(HEX_CHARS[urandom.getrandbits(4)] for _ in range(length))
        with open(path, "w") as f:
            f.write(uuid)
        return uuid


def wifi_scan_loop(folder="signals", interval=3):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    for iteration in range(999999):
        # print(f"{iteration} Thread: scanning Wi-Fi...")
        start_time = time.time()

        with open(f"{folder}/iteration", "w") as f:
            f.write(f"{iteration}")

        nets = wlan.scan()
        giraffe_nets = {}

        for net in nets:
            ssid = net[0].decode()
            if ssid.startswith("giraffe"):
                bssid = net[1]
                gfid = str(ssid).replace(NETWORK_PREFIX, "")
                channel = net[2]
                RSSI = net[3]
                authmode = net[4]
                hidden = net[5]

                line = f"{iteration},{start_time},{ssid},{gfid},{RSSI},{channel},{authmode},{bool(hidden)}"
                # print("→", line)
                giraffe_nets[gfid] = f"{RSSI}"

        write_time = time.time()
        for _id in giraffe_nets.keys():
            write_string = f"{iteration},{write_time},{giraffe_nets[_id]}\n"
            with open(f"{folder}/{_id}", "w") as f:
                f.write(write_string)
        end_time = time.time()
        wait_time = max(interval - (end_time - start_time), 0)
        # print(f"wait time to maintain {interval} second loop is {wait_time}")
        time.sleep(wait_time)


def configure_network():
    # Create an access point interface
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    # Configure the network name (SSID), password, channel, etc.
    device_id = _get_or_create_short_uuid()
    broadcast_network = NETWORK_PREFIX + device_id
    print("device network:", broadcast_network)
    ap.config(essid=broadcast_network, password='12345678', authmode=3)  # WPA2

