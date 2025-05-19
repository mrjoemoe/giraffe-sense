


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
from pubsub import EventBus


# led = Pin(4, Pin.OUT)  # D2 = GPIO2

led = PWM(Pin(4))
led.freq(1000)  # Set PWM frequency (Hz)

RSSI_MIN = -100
RSSI_MAX = -20
ATTENTUATION = 4
# K_CONST = 1 / (RSSI_MAX - RSSI_MIN)


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
    device_strength_dB = {}
    device_strength_normalized = {}
    if signal_queues:
        for device, values in signal_queues.items():
            if len(values) > 0:
                device_strength_dB[device] = sum(values) / len(values)
                print(f"'{device}' avg rssi = {device_strength_dB[device]}")
                device_strength_normalized[device] = signal_strength_to_normalized(device_strength_dB[device])
                print(f"'{device}' normalized rssi = {device_strength_normalized[device]}")
        device_average = sum(device_strength_normalized.values()) / len(device_strength_normalized)
        return device_average
    else:
        return RSSI_MIN


def blink_loop():
    """ Translate dB values in queues to duty cycle
    """

    while True:

        strength = get_signal_strength()  # value between 0 and 1
        # rssi_bound = min(max(signal_string, RSSI_MIN), RSSI_MAX)
        # strength = (100 - (rssi_bound * -1)) * K_CONST * (1 / ATTENTUATION)
        # s_atten = strength * K_CONST * (1 / ATTENTUATION)
        max_duty = strength * (1 / ATTENTUATION)  # leds are too bright so attenuate

        # convert to duty cycle signals
        duty_int = max(1, int(1024 * max_duty))
        duty_jumps = max(1, int(10 * max_duty))

        # our duty_int changes so we need to adjust the duty_change_delay between iterations
        # for the pulse to be consistent
        duty_change_delay = 0.002 / max(max_duty, 0.01)

        print(f"strength: {strength}")
        print(f"max_duty: {max_duty}")


        # Fade in
        for duty in range(0, duty_int, 1):  # 0 to 1023
            led.duty(duty)
            time.sleep(duty_change_delay)

        time.sleep(1.5)

        # Fade out
        for duty in range(duty_int -1, -1, -1 * 1):
            led.duty(duty)
            time.sleep(duty_change_delay)


def update_queues(folder="signals", last_iteration=-1):
    """ Pull data from files - add to signal queues
    """
    
    try:
        with open(f"{folder}/iteration", "r") as f:
            current_iteration = int(f.readlines()[0].strip())
    except OSError:
        current_iteration = -1

    # # no new data - exit early
    # if current_iteration == last_iteration:
    #     return current_iteration

    # Scan folder and process signal files - append to queues
    for fname in os.listdir(folder):

        # skip iteration file
        if fname == "iteration":
            continue

        # Add to signal queue
        if fname not in signal_queues.keys():
            signal_queues[fname] = deque((), 5)

        fpath = f"{folder}/{fname}"
        with open(fpath, "r") as f:
            line = f.readlines()[0].strip()
        iteration, write_time, signal_dB = line.strip().split(",")
        iteration = int(iteration)
        write_time = int(write_time)
        signal_dB = int(signal_dB)
        if int(signal_dB) != -110:
            signal_dB = max(min(signal_dB, RSSI_MAX), RSSI_MIN)

        # Step 3: Prepare new line and overwrite file with min - in case we drop
        write_string = f"{iteration + 1},{time.time()},{RSSI_MIN - 10}\n"
        with open(fpath, "w") as f:
            f.write(write_string)

        # # if we miss reading a network signal - assume lost - report min value
        # if iteration - current_iteration > 2:
        #     signal_queues[fname].append(RSSI_MIN)
        #     continue

        signal_queues[fname].append(signal_dB)

    # Debug print all queues
    for k, q in signal_queues.items():
        print(f"{k}: recent dBs: {list(q)}")

    return current_iteration + 1


def led_loop(bus, interval=3):
    """ LED Loop

    Pull latest signal strengths from files - put in queue

    We update queues independent of signal reads in case we miss reading a signal
    """
    current_iteration = -1
    test_iter = -1
    while True:
        test_iter += 1
        bus.publish("test_update", test_iter)
        start = time.ticks_ms()  # Start time in ms
        current_iteration = update_queues(last_iteration=current_iteration)
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000  # In seconds
        remaining = interval - elapsed
        print(f"remaining time: {remaining}")
        time.sleep(max(remaining, 0))
