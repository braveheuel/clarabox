#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
Jukebox Daemon

* Listen on RFID Chips
* Control MPD via
* Get Controlled via GPIO
* Controll LEDs
* (Maybe) Controlleable via D-Bus
"""
import configparser
import asyncio
import rfid


cfg = configparser.ConfigParser()
cfg.read("/etc/clarabox.conf")


def handle_code(s):
    print("handle code", s)


def main():
    asyncio.run(rfid.run_reader_loop(cfg["RFID"]["evdevpath"], handle_code))


if __name__ == "__main__":
    main()
