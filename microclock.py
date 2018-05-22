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
        bright = {'0': 0, '1': self.bright}
        guide = bytes([max(0, self.bright - 4)])
        binary = '{:016b}'.format(self.stamp)
        px = bytes(bright[pixel] for pixel in binary)
        return b'%s%s%s%s%s%s%s%s%s%s%s\0%s\0%s\0%s%s%s\0\0%s%s%s\0' % (
                px[0:1], px[2:3], px[4:5], px[6:7], px[8:9],
                px[1:2], px[3:4], px[5:6], px[7:8], px[9:10],
                guide, guide, guide,
                px[10:11], px[12:13], px[14:15],
                px[11:12], px[13:14], px[15:16])


def run(start=0):
    from microbit import display, Image, running_time, sleep
    now = running_time()
    clock = Clock(start, 6)
    while True:
        display.show(Image(5, 5, clock.image_b()))
        now += 1000
        sleep(now - running_time())
        clock.tick()
