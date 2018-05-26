from microbit import (display, Image, running_time, sleep,
            button_a, button_b)

class Clock:
    skips = ((0xf, 0x1), (0x3c0, 0x40), (0xc000, -0xc000))

    def __init__(self, stamp=0, bright=9):
        self.stamp = stamp
        self.bright = bright
        self.now = running_time()

    def tick(self, rt=False):
        if rt:
            self.now += 988
            sleep(self.now - running_time())
        self.stamp += 1
        for mask, fix in self.skips:
            if self.stamp & mask == mask:
                self.stamp += fix

    def image_b(self, secs=True):
        bright = 0, self.bright
        guide = max(1, self.bright - 2) if self.bright else 0
        t = self.stamp if secs else (self.stamp & 0xffc0)
        px = [bright[pixel == '1'] for pixel in '{:016b}'.format(t)]
        return bytes(
                px[0:9:2] + px[1:10:2] +
                [guide, 0] * 3 +
                px[10::2] + [0, 0] + px[11::2] + [0])


def run(start=0):
    clock = Clock(start, 3)
    secs = True
    while True:
        if button_b.was_pressed():
            if clock.bright == 9:
                display.clear()
                display.off()
                while not button_b.was_pressed():
                    clock.tick(True)
                display.on()
                clock.bright = 1
            else:
                clock.bright += 1
        if button_a.was_pressed():
            secs = not secs
        display.show(Image(5, 5, clock.image_b(secs)))
        clock.tick(True)


if __name__ == '__main__':
    run(0)
