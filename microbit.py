"""
Test module to allow code using micro:bit libraries to run
outside a micro:bit.
"""

from unittest import mock

display = mock.Mock()
Image = mock.Mock()
running_time = mock.Mock()
sleep = mock.Mock()
button_a = mock.Mock()
button_b = mock.Mock()
