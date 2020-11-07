#! /usr/bin/env python
# * | File        :	  poll_test_now_button.py
# * | Author      :   HoChri (aka Legufix)
# * | Function    :   poll the state of the button on the front panel 
# * | Info        :
# *----------------
# * |	This version:   V0.4
# * | Date        :   2018-05-18


# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import bandwidth_monitor_0_4 as bw_monitor
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GREEN = 5
BLUE = 6
RED = 13

GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.output(GREEN, GPIO.HIGH)
GPIO.output(BLUE, GPIO.HIGH)
GPIO.output(RED, GPIO.HIGH)

TestNowButton = 16

GPIO.setup(TestNowButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == "__main__":
    # time.sleep(60)
    GPIO.output(RED, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RED, GPIO.HIGH)

    while True:
        try:
            print("waiting for button")
            GPIO.wait_for_edge(TestNowButton, GPIO.FALLING)

            print("Button pressed")
            bw_monitor.main()
        except KeyboardInterrupt:
            print("Fubar")
            GPIO.cleanup()
            break
    GPIO.cleanup()
