IMAGE_STR_FORMATTER = ':'.join(['%s' * 5]*5)

class Clock:
    skips = ((0xf, 0x1), (0x3c0, 0x40), (0xc000, -0xc000))

    def __init__(self, stamp=0, brightness=9):
        """
        Supply the time as a 16-bit binary value.
        Default noon/midnight.
        """
        self.stamp = stamp
        self.brightness = brightness

    def tick(self):
        self.stamp += 1
        for mask, fix in self.skips:
            if (self.stamp & mask) == mask:
                self.stamp += fix

    def image_bytes(self):
        bright = {'0': b'\0', '1': bytes([self.brightness])}
        helper = bytes([max(0, self.brightness - 4)])
        binary_str = f'{self.stamp:016b}'
        pix = [bright[pixel] for pixel in binary_str]
        return b'%s%s%s\0%s\0%s\0%s\0\0%s\0' % (
                pix[0] + pix[2] + pix[4] + pix[6] + pix[8],
                pix[1] + pix[3] + pix[5] + pix[7] + pix[9],
                helper, helper, helper,
                pix[10] + pix[12] + pix[14],
                pix[11] + pix[13] + pix[15])

    def image_str(self):
        return IMAGE_STR_FORMATTER % tuple(self.image_bytes())
