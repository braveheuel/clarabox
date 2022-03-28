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
import gpio
import devicecontroller


cfg = configparser.ConfigParser()
cfg.read("/etc/clarabox.conf")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("daemon")

async def main():
    logger.info("Init the MusicController...")
    loop = asyncio.get_event_loop()
    btn_queue = asyncio.Queue(cfg["GPIO"].getint("max_events", 10))
    mpdc = mpdcontroller.MusicController(cfg,
                                         btn_queue)
    gpioc = gpio.GPIOController(cfg["GPIO_MAP"], btn_queue,
                                cfg.getfloat("GPIO", "debounce_time",
                                             fallback=None),
                                loop=loop)
    devicec = devicecontroller.DeviceController(mpdc, cfg["MPD"].getint("idle_time", 15))

    logger.info("Start the Async Gathering...")
    await asyncio.gather(mpdc.connect_mpd(),
                         rfid.run_reader_loop(cfg["RFID"]["evdevpath"],
                                              mpdc.play_card),
                         devicec.run_periodically_status(),
                         loop=loop
                         )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
                logger.info("Process interrupted")
