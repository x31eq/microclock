class Clock:
    skips = ((0xf, 0x1), (0x3c0, 0x40), (0xc000, -0xc000))

    def __init__(self, stamp=0, bright=9):
        self.stamp = stamp
        self.bright = bright

    def tick(self):
        self.stamp += 1
        for mask, fix in self.skips:
            if (self.stamp & mask) == mask:
                self.stamp += fix

    def image_b(self):
        bright = 0, self.bright
        guide = max(1, self.bright - 3)
        binary = '{:016b}'.format(self.stamp)
        px = [bright[pixel == '1'] for pixel in binary]
        return bytes(
                px[0:9:2] + px[1:10:2] +
                [guide, 0, guide, 0, guide] +
                [0] + px[10::2] + [0] +
                [0] + px[11::2] + [0])


def run(start=0):
    from microbit import display, Image, running_time, sleep
    now = running_time()
    clock = Clock(start, 5)
    while True:
        display.show(Image(5, 5, clock.image_b()))
        now += 1000
        sleep(now - running_time())
        clock.tick()

if __name__ == '__main__':
    run()
