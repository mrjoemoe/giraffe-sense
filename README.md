# giraffe-sense
just a silly repo for a silly purpose


## xiao esp32-c3

micropython
```bash
port (example): /dev/cu.usbmodem101
```


### Flash
```bash
esptool.py --chip esp32c3 --port /dev/cu.usbmodem1101 erase_flash
esptool.py --chip esp32c3 --port /dev/cu.usbmodem1101 --baud 460800 write_flash -z 0x0 ESP32_GENERIC_C3-20250415-v1.25.0.bin
```

### Uploading Files
```bash
mpremote connect /dev/cu.usbmodem1101 cp boot.py :boot.py
mpremote connect /dev/cu.usbmodem1101 cp main.py :main.py
mpremote connect /dev/cu.usbmodem1101 cp giraffe_net.py :giraffe_net.py
mpremote connect /dev/cu.usbmodem1101 cp led_driver.py :led_driver.py
mpremote connect /dev/cu.usbmodem1101 cp pubsub.py :pubsub.py
mpremote connect /dev/cu.usbmodem1101 cp battery.py :battery.py
mpremote connect /dev/cu.usbmodem1101 cp ticker.py :ticker.py
```

### Upload all files
```bash
mpremote connect /dev/cu.usbmodem1101 cp boot.py :boot.py && mpremote connect /dev/cu.usbmodem1101 cp main.py :main.py && mpremote connect /dev/cu.usbmodem1101 cp giraffe_net.py :giraffe_net.py && mpremote connect /dev/cu.usbmodem1101 cp led_driver.py :led_driver.py && mpremote connect /dev/cu.usbmodem1101 cp pubsub.py :pubsub.py && mpremote connect /dev/cu.usbmodem1101 cp battery.py :battery.py && mpremote connect /dev/cu.usbmodem1101 cp ticker.py :ticker.py
```

### Reset and stream stdout to console
```bash
mpremote connect /dev/cu.usbmodem1101 reset repl
```


## Todo
(software)
- add time keeper function - manage in a single function - ensure loops are synchronized
- party mode routine - goes off when joining up with people after being alone
- startup routine
- monitors
    - memory
    - battery
    - temp?

(hardware)
- inputs:
  - max friends adjuster (max number of other devices to use signal strength)
  - blink mode - continuous vs pulse


(general)
- only sync to friends you care about
- OTA updates on playa? (maybe not necessary)


## BOM
- (cpu) seeed studio xiao esp32c3
- (battery) <lipo>
- (led board - dev) - https://www.amazon.com/cart/smart-wagon?newItems=7f687e61-9ff9-4ba9-a3ef-7552ec4b583e,2&ref_=sw_refresh



## Battery
how to check - https://wiki.seeedstudio.com/check_battery_voltage/
