IMG_FMT = ':'.join(['%s' * 5]*5)

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
        bright = {'0': b'\0', '1': bytes([self.bright])}
        helper = bytes([max(0, self.bright - 4)])
        binary_str = f'{self.stamp:016b}'
        px = [bright[pixel] for pixel in binary_str]
        return b'%s%s%s\0%s\0%s\0%s\0\0%s\0' % (
                px[0] + px[2] + px[4] + px[6] + px[8],
                px[1] + px[3] + px[5] + px[7] + px[9],
                helper, helper, helper,
                px[10] + px[12] + px[14],
                px[11] + px[13] + px[15])

    def image_s(self):
        return IMG_FMT % tuple(self.image_b())
