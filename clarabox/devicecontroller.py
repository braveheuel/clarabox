#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Christoph Heuel <christoph@heuel-web.de>
#
# Distributed under terms of the MIT license.

"""
Device Controller Class

This Class controls the entire Device, eg. Powering it off, etc
"""
import asyncio
import logging

class DeviceController:
    """ Device Controller Class
    """

    def __init__(self, mpd, idle_time):
        self.mpd = mpd
        self.interval = 60
        self.idle_counter = 0
        self.idle_time = idle_time

    async def run_periodically_status(self):
        while True:
            await asyncio.gather(
                    asyncio.sleep(self.interval),
                    self._check_mpd(),
                )
    
    async def _check_mpd(self):
        try:
            status = await self.mpd.status()
        except:
            logging.info("Could not get status, continueing")
            return
        if status["state"] == "play":
            self.idle_counter = 0
            logging.debug("Counter Reset to 0")
        else:
            self.idle_counter += 1
            logging.debug("Counter set to %d", self.idle_counter)

        if self.idle_counter >= self.idle_time:
            logging.info("Reached Idle Counter, turning off Unit! (%d)", self.idle_time)
            await self._poweroff()

    async def _poweroff(self):
        await asyncio.create_subprocess_shell("sudo systemctl poweroff")


