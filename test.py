#!/usr/bin/env python3

"""
Desktop tests for MicroPython code
"""

import clock as microclock
import time

IMAGE_FORMAT = '\n'.join(['%s' * 5]*5)


def tick_test(start=None, wait=1000, bright=8):
    if start is None:
        start = unix_to_micro()
    clock = microclock.Clock(start, bright)
    while True:
        clock.tick()
        print(f'{clock.stamp:04x}')
        print(IMAGE_FORMAT % tuple(clock.image_b()))
        time.sleep(wait / 1000)
        print()


def unix_to_micro(unix_stamp=None):
    if unix_stamp is None:
        unix_stamp = time.time()
    time_struct = time.localtime(unix_stamp)
    return hms_to_micro(
            (time_struct.tm_hour % 12),
            time_struct.tm_min,
            time_struct.tm_sec)


def hms_to_micro(hour, minute, sec):
    result = hour << 12
    result += (minute + minute // 15) << 6
    result += sec + sec // 15
    return result


if __name__ == '__main__':
    clock = microclock.Clock()
    assert clock.stamp == 0, clock.stamp
    clock.tick()
    assert clock.stamp == 1, clock.stamp

    current_time = clock.stamp
    for sec in range(59):
        clock.tick()
        assert clock.stamp > current_time
        current_time = clock.stamp
    assert clock.stamp == 0x40, clock.stamp

    clock = microclock.Clock()
    for minute in range(60):
        for sec in range(60):
            clock.tick()
        assert clock.stamp & 0x3f == 0, clock.stamp
    assert clock.stamp == 0x1000, clock.stamp

    clock = microclock.Clock(hms_to_micro(11, 0, 0))
    for minute in range(60):
        for sec in range(60):
            clock.tick()
        assert clock.stamp & 0x3f == 0, clock.stamp
    assert clock.stamp == 0, clock.stamp

    tick_test(bright=7)
