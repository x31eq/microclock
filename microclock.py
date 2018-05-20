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
        px = bytes(bright[pixel] for pixel in f'{self.stamp:016b}')
        return px[:9:2] + px[1:10:2] + b'%s\0%s\0%s\0%s\0\0%s\0' % (
                guide, guide, guide, px[10::2], px[11::2])
