from machine import Pin
import time

# D2 on XIAO ESP32-C3 maps to GPIO6
led = Pin(6, Pin.OUT)

while True:
    led.value(1)  # Turn LED on
    time.sleep(1)  # Delay 1 second
    led.value(0)  # Turn LED off
    time.sleep(1)


