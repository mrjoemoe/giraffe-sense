


""" led_driver.py

Scan networks for network
  - capture unique network ID, ie name
  - on each scan save: network name - strength - iteration -> dump into files for each device under signal folder
  - dump last iteration to its own file

led driver
  - check for signal strength files
  - read last iteration number
  - read strength from files
  - translate each dB to score
  - add up all score - scale - translate to duty cycle

"""


import os
import time
from collections import deque
from machine import Pin, PWM
import math


# led = Pin(4, Pin.OUT)  # D2 = GPIO2

led = PWM(Pin(4))
led.freq(1000)  # Set PWM frequency (Hz)

RSSI_MIN = -100
RSSI_MAX = -20
ATTENTUATION = 4
K_CONST = 1 / (RSSI_MAX - RSSI_MIN)


signal_queues = {}


def signal_strength_to_normalized(rssi):
    # Shift and scale RSSI to fit sigmoid curve
    # Center point at -60 (0.5), curve steepness controlled by factor
    k = 0.3  # Steepness factor (higher = steeper curve)
    x0 = -60  # Midpoint where output ≈ 0.5

    # Standard sigmoid: 1 / (1 + e^(-k(x - x0)))
    norm = 1 / (1 + math.exp(-k * (rssi - x0)))
    return norm


# should probably make a generator
def get_signal_strength():
    devices = {}
    if signal_queues:
        for device, values in signal_queues.items():
            if len(values) > 0:
                devices[device] = sum(values) / len(values)
                print(f"avg rssi = {devices[device]}")
                normalized = signal_strength_to_normalized(devices[device])
                print(f"normalized rssi = {normalized}")
                return normalized
    else:
        return RSSI_MIN


def blink_loop():
    """ Main loop - run continually with updates to signal_strength
    """

    while True:

        strength = get_signal_strength()
        # rssi_bound = min(max(signal_string, RSSI_MIN), RSSI_MAX)
        # strength = (100 - (rssi_bound * -1)) * K_CONST * (1 / ATTENTUATION)
        strength_adj = strength * K_CONST * (1 / ATTENTUATION)
        strength_adj = strength * (1 / ATTENTUATION)
        max_duty = max(1, int(1024 * strength_adj))
        duty_jumps = max(1, int(10 * strength_adj))
        delay = 0.002 / max(strength_adj, 0.01)

        print(f"strength: {strength}")
        print(f"strength_adj: {strength_adj}")

        # led.duty(max_duty)
        # time.sleep(1)

        # Fade in
        for duty in range(0, max_duty, 1):  # 0 to 1023
            led.duty(duty)
            time.sleep(delay)

        time.sleep(1.5)

        # Fade out
        for duty in range(max_duty -1, -1, -1 * 1):
            led.duty(duty)
            time.sleep(delay)


def update_queues(folder="signals", last_iteration=-1):
    """ 
    """
    
    try:
        with open(f"{folder}/iteration", "r") as f:
            current_iteration = int(f.readlines()[0].strip())
    except OSError:
        current_iteration = -1

    if current_iteration == last_iteration:
        return current_iteration

    # 2. Scan folder and process signal files
    for fname in os.listdir(folder):

        # skip iteration file
        if fname == "iteration":
            continue

        # 4. Add to signal queue
        if fname not in signal_queues.keys():
            signal_queues[fname] = deque((), 5)

        fpath = f"{folder}/{fname}"
        with open(fpath, "r") as f:
            line = f.readlines()[0].strip()
        iteration, write_time, signal_dB = line.strip().split(",")
        iteration = int(iteration)
        write_time = int(write_time)
        signal_dB = int(signal_dB)

        # if we miss reading a network signal - assume lost - report min value
        if iteration - current_iteration > 2:
            signal_queues[fname].append(RSSI_MIN)
            continue

        signal_queues[fname].append(signal_dB)

    # Debug print all queues
    for k, q in signal_queues.items():
        print(f"{k}: recent dBs: {list(q)}")

    return current_iteration


def signals_loop(interval=3):
    current_iteration = -1
    while True:
        start = time.ticks_ms()  # Start time in ms
        current_iteration = update_queues(last_iteration=current_iteration)
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000  # In seconds
        remaining = interval - elapsed
        print(f"remaining time: {remaining}")
        time.sleep(max(remaining, 0))
