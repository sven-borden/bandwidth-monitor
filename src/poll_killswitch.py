#! /usr/bin/env python
# * | File        :	  poll_killswitch.py
# * | Author      :   HoChri (aka Legufix)
# * | Function    :   poll the remote reset button
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

import requests
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
RELAIS_1 = 21
GPIO.setup(RELAIS_1,GPIO.OUT)
GPIO.output(RELAIS_1,GPIO.HIGH)

GREEN = 5
BLUE = 6
RED = 13

GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
#GPIO.output(GREEN,GPIO.HIGH)
#GPIO.output(BLUE,GPIO.HIGH)
#GPIO.output(RED,GPIO.HIGH)


TOKEN = "XXXXXXXXXXXXXXXXXXXX"  # Put your TOKEN here
DEVICE = "raspberry-bandwidth-monitor"  # Put your device label here
VARIABLE = "killswitch"  # Put your first variable label here
VARIABLE_2 = "reset-code"  # Put your second variable label here

print_messages = False
killSwitch_state = 0

def get_var(device, variable):
    try:
        url = "http://things.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        if print_messages:
            print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    if print_messages:
        print("[INFO] request made properly, your device is updated")
    return True

if __name__ == "__main__":
    GPIO.output(GREEN,GPIO.LOW)
    killSwitch_state=get_var(DEVICE, VARIABLE)
    GPIO.output(GREEN,GPIO.HIGH)
    if print_messages:
        print("Kill switch state: %d" % killSwitch_state)
    if killSwitch_state == 1.0:
        GPIO.output(RELAIS_1,GPIO.LOW)
        if print_messages:
            print('kill em all')
        time.sleep(5)
        GPIO.output(RELAIS_1,GPIO.HIGH)
        time.sleep(60)
        post_request({VARIABLE: 0.0, VARIABLE_2: 1.0})
