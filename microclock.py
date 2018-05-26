from microbit import (display, Image, running_time, sleep,
            button_a, button_b)

class Clock:
    skips = ((0xf, 0x1), (0x3c0, 0x40), (0xc000, -0xc000))

    def __init__(self, stamp=0, bright=9):
        self.stamp = stamp
        self.bright = bright

    def tick(self):
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


class App:
    def __init__(self, start=0):
        self.clock = Clock(start, 3)
        self.secs = True
        self.now = running_time()

    def tick(self):
        self.now += 988
        sleep(self.now - running_time())
        self.clock.tick()

    def run(self):
        while True:
            if button_b.was_pressed():
                if self.clock.bright == 9:
                    display.clear()
                    display.off()
                    while not button_b.was_pressed():
                        self.tick()
                    display.on()
                    self.clock.bright = 1
                else:
                    self.clock.bright += 1
            if button_a.was_pressed():
                self.secs = not self.secs
            display.show(Image(5, 5, self.clock.image_b(self.secs)))
            self.tick()


if __name__ == '__main__':
    App().run()
