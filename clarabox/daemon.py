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
import mpdcontroller
import logging


cfg = configparser.ConfigParser()
cfg.read("/etc/clarabox.conf")
logging.basicConfig(level=logging.DEBUG)


async def main():
    logging.info("Init the MusicController...")
    mpdc = mpdcontroller.MusicController(cfg["MPD"]["host"],
                                         cfg["MPD"].get("port", None),
                                         cfg["RFID"]["mapping"],
                                         int(cfg["RFID"]["reswipe_time"]))
    logging.info("Start the Async Gathering...")
    await asyncio.gather(mpdc.connect_mpd(),
                         rfid.run_reader_loop(cfg["RFID"]["evdevpath"],
                                              mpdc.play_card)
                         )


if __name__ == "__main__":
    asyncio.run(main())
