#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
GPIO module
"""
import asyncio
import logging
import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory


gpiozero.Device.pin_factory = PiGPIOFactory()

class GPIOController:

    def __init__(self, gpiomap, queue, debounce_time, loop):
        self.gpiomap = gpiomap
        self.queue = queue
        self.debounce_time = debounce_time
        self.btnstrmap = {}
        self._setup_gpios()
        self.loop = loop;

    def _setup_gpios(self):
        self.btnmap = {}
        for i in self.gpiomap:
            btn_name = self.gpiomap[i].lower()
            if not btn_name.startswith("none"):
                self.btnmap[btn_name] = gpiozero.Button(btn_name,
                                                        pull_up=None,
                                                        active_state=False,
                                                        bounce_time=
                                                        self.debounce_time)
                self.btnmap[btn_name].when_released = self._callback;
                self.btnstrmap[btn_name] = i

    def _callback(self, btn):
        name = str(btn.pin).lower()
        logging.info("Cmd: %s", self.btnstrmap[name])
        try:
            self.loop.call_soon_threadsafe(self.queue.put_nowait,
                                            self.btnstrmap[name])
        except asyncio.QueueFull:
            logging.warning("Button event %s missed, Event Queue full!",
                            self.btnstrmap[name])

if __name__ == "__main__":
    from signal import pause
    logging.warning("%s", gpiozero.Device.pin_factory)
    gpioc = GPIOController({"next":"gpio23"}, None, 0.010)
    pause()
