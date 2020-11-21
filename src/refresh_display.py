#! /usr/bin/env python

import epd2in9
from PIL import Image, ImageFont, ImageDraw
import time

COLORED = 0
UNCOLORED = 1

numberofcycles = 3


def main():

    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)
    image = Image.new('1', (epd2in9.EPD_HEIGHT, epd2in9.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)
    for i in range(0, numberofcycles):

        draw.rectangle((0, 0, epd2in9.EPD_HEIGHT, epd2in9.EPD_WIDTH), fill=COLORED)
        epd.clear_frame_memory(0xFF)
        epd.set_frame_memory(image.rotate(270,expand=True), 0, 0)
        epd.display_frame()
        time.sleep(1)

        draw.rectangle((0, 0, epd2in9.EPD_HEIGHT, epd2in9.EPD_WIDTH), fill=UNCOLORED)
        epd.clear_frame_memory(0xFF)
        epd.set_frame_memory(image.rotate(270, expand=True), 0, 0)
        epd.display_frame()
        time.sleep(1)


if __name__ == '__main__':
    main()
