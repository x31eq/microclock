#!/usr/bin/env python3

"""
Desktop tests for MicroPython code
"""

import microclock

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

    clock = microclock.Clock(0xb000)
    for minute in range(60):
        for sec in range(60):
            clock.tick()
        assert clock.stamp & 0x3f == 0, clock.stamp
    assert clock.stamp == 0, clock.stamp
