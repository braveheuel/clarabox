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

    def __init__(self, gpiomap, queue, debounce_time):
        self.gpiomap = gpiomap
        self.queue = queue
        self.debounce_time = debounce_time
        self._setup_gpios()

    def _setup_gpios(self):
        self.btnmap = {}
        for i in self.gpiomap:
            btn_name = self.gpiomap[i].lower()
            if not btn_name.startswith("none"):
                logging.info("%s: %s", i, self.gpiomap[i])
                self.btnmap[btn_name] = gpiozero.Button(btn_name,
                                                        pull_up=None,
                                                        active_state=False,
                                                        bounce_time=
                                                        self.debounce_time)
                self.btnmap[btn_name].when_pressed = self._callback

    def _callback(self, btn):
        logging.warning("Button pressed! %s", btn)

if __name__ == "__main__":
    from signal import pause
    logging.warning("%s", gpiozero.Device.pin_factory)
    gpioc = GPIOController({"next":"gpio23"}, None, 0.010)
    pause()
