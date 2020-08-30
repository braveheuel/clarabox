#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
LED Daemon (should run with root permissions)
"""
import configparser

cfg = configparser.ConfigParser()
cfg.read("/etc/clarabox.conf")

def main():
    LED_COUNT = cfg["WS8211"].getint("count", 6)
    LED_PIN =  cfg["WS8211"].getint("pin", 12)
    LED_FREQ_HZ = cfg["WS8211"].getint("frequence", 800000)
    LED_DMA = cfg["WS8211"].getint("dma", 10)
    LED_INVERT = cfg["WS8211"].getboolean("invert", False)
    LED_BRIGHTMESS = cfg["WS8211"].getint("brightness", 255)
    LED_CHANNEL = cfg["WS8211"].getint("channel", 0)
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()




if __name__ == "__main__":
    main()
