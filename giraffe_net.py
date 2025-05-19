import network
import time
import urandom
import os


HEX_CHARS = "0123456789abcdef"
NETWORK_PREFIX = "giraffenet-"
SCAN_REPEATS = 2

def _get_or_create_short_uuid(path="uuid.txt", length=8):
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


def scan_loop(folder="signals", interval=3):
    """ Scan for wifi networks
    If network starts with 'giraffe' save data to folder.
    """

    wlan = network.WLAN(network.STA_IF)

    for iteration in range(999999):
        # print(f"{iteration} Thread: scanning Wi-Fi...")
        start_time = time.time()

        wlan.active(False)
        time.sleep(0.1)
        wlan.active(True)

        with open(f"{folder}/iteration", "w") as f:
            f.write(f"{iteration}")

        giraffe_nets = {}

        found_gfids = []

        for _ in range(SCAN_REPEATS):
            nets = wlan.scan()
            for net in nets:
                ssid = net[0].decode()
                if ssid.startswith("giraffe"):
                    gfid = str(ssid).replace(NETWORK_PREFIX, "")
                    if gfid in found_gfids:
                        continue
                    else:
                        found_gfids.append(gfid)
                    bssid = net[1]
                    channel = net[2]
                    rssi = net[3]
                    authmode = net[4]
                    hidden = net[5]

                    line = f"{iteration},{start_time},{ssid},{gfid},{rssi},{channel},{authmode},{bool(hidden)}"
                    # print("→", line)
                    giraffe_nets[gfid] = f"{rssi}"

        write_time = time.time()
        for _id in giraffe_nets.keys():
            write_string = f"{iteration},{write_time},{giraffe_nets[_id]}\n"
            with open(f"{folder}/{_id}", "w") as f:
                f.write(write_string)
        end_time = time.time()
        wait_time = max(interval - (end_time - start_time), 0)
        print(f"abc123 {end_time - start_time}")
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

