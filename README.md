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
```

### Reset and stream stdout to console
```bash
mpremote connect /dev/cu.usbmodem1101 reset repl
```
