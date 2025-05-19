import machine

adc = machine.ADC(machine.Pin(10))  # Battery voltage pin on XIAO ESP32-C3
adc.atten(machine.ADC.ATTN_11DB)    # Up to ~3.3V range

def read_battery_voltage():
    raw = adc.read()
    voltage = raw / 4095 * 3.3  # Adjust if using a divider
    return voltage
