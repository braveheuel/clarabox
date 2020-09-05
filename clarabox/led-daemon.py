#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
LED Daemon (should run with root permissions)
"""
import configparser
import asyncio
from rpi_ws281x import PixelStrip, Color

cfg = configparser.ConfigParser()
cfg.read("/etc/clarabox.conf")

strip = None

def init():
    global strip
    LED_COUNT = cfg["WS8211"].getint("count", 6)
    LED_PIN =  cfg["WS8211"].getint("pin", 12)
    LED_FREQ_HZ = cfg["WS8211"].getint("frequence", 800000)
    LED_DMA = cfg["WS8211"].getint("dma", 10)
    LED_INVERT = cfg["WS8211"].getboolean("invert", False)
    LED_BRIGHTNESS = cfg["WS8211"].getint("brightness", 50)
    LED_CHANNEL = cfg["WS8211"].getint("channel", 0)
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()


def main():
    init()

    strip.setPixelColor(0, Color(255, 0, 0))
    strip.setPixelColor(1, Color(255, 255, 0))
    strip.setPixelColor(2, Color(255, 255, 255))
    strip.setPixelColor(3, Color(0, 255, 0))
    strip.setPixelColor(4, Color(0, 255, 255))
    strip.setPixelColor(5, Color(255, 255, 255))
    strip.show()



if __name__ == "__main__":
    main()
