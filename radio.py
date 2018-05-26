"""
Mock the micro:bit radio module
"""
from unittest import mock

on = mock.Mock()
off = mock.Mock()
config = mock.Mock()
send_bytes = mock.Mock()
receive_bytes = mock.Mock()
