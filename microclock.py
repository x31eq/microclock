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
        binary_str = f'{self.stamp:016b}'
        return '{}{}{}{}{}:{}{}{}{}{}:20202:0{}{}{}0:0{}{}{}0'.format(
                binary_str[0], binary_str[2], binary_str[4],
                    binary_str[6], binary_str[8],
                binary_str[1], binary_str[3], binary_str[5],
                    binary_str[7], binary_str[9],
                binary_str[10], binary_str[12], binary_str[14],
                binary_str[11], binary_str[13], binary_str[15])
