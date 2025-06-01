import machine, neopixel, time

# Pin setup
NUM_LEDS = 5                  # Change to your number of LEDs
PIN_NUM = 4                   # 4 = D2 → GPIO2
pin = machine.Pin(PIN_NUM)
leds = neopixel.NeoPixel(pin, NUM_LEDS)

# Simple gamma correction
gamma_table = [min(int((i / 255) ** 2.8 * 255), 255) for i in range(256)]

BRIGHTNESS = 0.1  # between 0 and 1

def gamma(x):
    return gamma_table[x]

def fade_led(color=(255, 0, 0), delay=0.02):

    def _fade_inner_loop(index, color_inner=(0, 0, 255), delay_inner=0.02):
        for b in range(0, 256, 5):
            leds[index] = tuple(int(c * b * BRIGHTNESS/ 255) for c in color_inner)
            leds.write()
            time.sleep(delay_inner)
        # Fade out
        for b in range(255, -1, -5):
            leds[index] = tuple(int(c * b * BRIGHTNESS / 255) for c in color_inner)
            leds.write()
            time.sleep(delay_inner)

    while True:
        for i in range(NUM_LEDS):
            _fade_inner_loop(i, color_inner=(0, 0, 255), delay_inner=delay)  # Fade each LED in sequence



def rainbow_fade(delay=0.02, steps=256):
    """ All leds cycle through colors together
    """

    def _fill(r, g, b):
        for i in range(NUM_LEDS):
            leds[i] = (r, g, b)
        leds.write()
        time.sleep(0.001)


    while True:
        for i in range(steps):
            r = gamma(255 - i)
            g = gamma(i)
            _fill(r, g, 0)
            if i % 20 == 0:
                print(f"fade RG {i}")
            time.sleep(delay)

        for i in range(steps):
            g = gamma(255 - i)
            b = gamma(i)
            _fill(0, g, b)
            if i % 20 == 0:
                print(f"fade GB {i}")
            time.sleep(delay)

        for i in range(steps):
            b = gamma(255 - i)
            r = gamma(i)
            _fill(r, 0, b)
            if i % 20 == 0:
                print(f"fade BR {i}")
            time.sleep(delay)


def crossfade(color=(0,0,255)):
    # Triangle wave brightness function
    def inverted_triangle_wave(x):
        if x < 128:
            return int(255 - 2 * x) * BRIGHTNESS
        else:
            return int(2 * x - 255) * BRIGHTNESS

    def set_leds(step, set_color=(0, 0, 255)):
        for i in range(NUM_LEDS):
            # Offset each LED by part of the cycle
            offset = (step + i * (256 // NUM_LEDS)) % 256
            brightness = inverted_triangle_wave(offset)
            r = int(set_color[0] * brightness / 255)
            g = int(set_color[1] * brightness / 255)
            b = int(set_color[2] * brightness / 255)
            leds[i] = (r, g, b)
        leds.write()

    # Main loop
    while True:
        for step in range(256):
            set_leds(step, set_color=color)  # Smooth blue wave
            time.sleep(0.01)
