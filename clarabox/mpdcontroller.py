"""MPD Controller"""
import csv
import mpd

_mpc = None
_rfid_map = None
_swipe_timeout = None

def init_player(host, port, rfid_map, swipe_timeout):
    _mpc = mpd.MPDClient(host, port)

