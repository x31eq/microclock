import radio
from microbit import (display, Image, sleep,
        running_time, button_a, button_b, temperature)

def run(start=0):
    clock = Clock(start)
    screen = Screen(3)
    mode = 0
    secs = True
    while True:
        if button_b.was_pressed():
            if screen.bright == 9:
                clock.hide(button_b)
                screen.bright = 1
            else:
                screen.bright += 1
        if button_a.was_pressed():
            mode += 1
            if mode == 3:
                clock.hide(button_a)
                mode = 0
        m, s = clock.minsec()
        screen.show(m,
                s if mode == 0 else 0 if mode == 1 else temperature(),
                7 if mode == 2 else 0x15)
        clock.tick(True)


class Screen:
    def __init__(self, bright=5):
        self.bright = bright
        display.on()

    def show(self, top, bot, guides=0x15):
        bright = str(self.bright)
        guide = str(max(1, self.bright - 2))
        gx = list(map(int, '{:05b}'.format(guides).replace('1', guide)))
        tx, bx = (list(map(int, '{:010b}'.format(px).replace('1', bright)))
                for px in (top, bot))
        display.show(Image(5, 5, bytes(
                tx[0::2] + tx[1::2] + gx + bx[0::2] + bx[1::2])))


class Clock:
    skips = ((0xf, 0x1), (0x3c0, 0x40), (0xc000, -0xc000))

    def __init__(self, stamp=0, bright=9):
        self.stamp = stamp
        self.now = running_time()
        radio.config(channel=18, address=0x867fa897, length=3, queue=1)
        radio.on()
        self.time_set = False

    def tick(self, rt=False):
        try:
            message = radio.receive_bytes()
            if not self.time_set and message and message[0] == 1:
                self.stamp = int.from_bytes(message[1:], 2, 'big')
                radio.off()
                self.time_set = True
        except Exception:
            pass
        if rt:
            self.now += 988
            sleep(self.now - running_time())
        self.stamp += 1
        for mask, fix in self.skips:
            if self.stamp & mask == mask:
                self.stamp += fix

    def minsec(self):
        return self.stamp >> 6, (self.stamp & 0x3f) << 2

    def hide(self, unhider):
        display.clear()
        display.off()
        while not unhider.was_pressed():
            self.tick(True)
        display.on()


if __name__ == '__main__':
    run(0)
