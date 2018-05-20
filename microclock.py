class Clock:
    skips = ((0xf, 0x1), (0x3c0, 0x40), (0xc000, -0xc000))

    def __init__(self, stamp=0):
        """
        Supply the time as a 16-bit binary value.
        Default noon/midnight.
        """
        self.stamp = stamp

    def tick(self):
        self.stamp += 1
        for mask, fix in self.skips:
            if (self.stamp & mask) == mask:
                self.stamp += fix

    def image_str(self):
        bright = {'0': '0', '1': '9'}
        binary_str = f'{self.stamp:016b}'
        pix = [bright[pixel] for pixel in binary_str]
        return '{}{}{}{}{}:{}{}{}{}{}:20202:0{}{}{}0:0{}{}{}0'.format(
                pix[0], pix[2], pix[4], pix[6], pix[8],
                pix[1], pix[3], pix[5], pix[7], pix[9],
                pix[10], pix[12], pix[14],
                pix[11], pix[13], pix[15])
