import epd2in9
from PIL import Image, ImageFont, ImageDraw
import speedtest
import time
import json
import requests

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
RELAIS_1 = 21
GPIO.setup(RELAIS_1, GPIO.OUT)
GPIO.output(RELAIS_1, GPIO.HIGH)

GREEN = 5
BLUE = 6
RED = 13

GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.output(GREEN, GPIO.HIGH)
GPIO.output(BLUE, GPIO.HIGH)
GPIO.output(RED, GPIO.HIGH)

with open('config.json') as f:
    j = json.load(f)
    TOKEN = j['token']
    DEVICE_LABEL = j['device']

VARIABLE_LABEL_1 = "Upload"  # Put your first variable label here
VARIABLE_LABEL_2 = "Download"  # Put your first variable label here
VARIABLE_LABEL_3 = "Ping"  # Put your first variable label here
VARIABLE = "killswitch"  # Put your first variable label here
VARIABLE_2 = "reset-code"  # Put your second variable label here

COLORED = 0

print_messages = False

lower_limit = 5000000  # Threshold for download speed -> modem will be reseted
max_iterations = 3


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        try:
            req = requests.post(url=url, headers=headers, json=payload)
            status = req.status_code
            attempts += 1
            time.sleep(1)
        except:
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


def green_LED_on(state):
    if state is True:
        GPIO.output(GREEN, GPIO.LOW)
    else:
        GPIO.output(GREEN, GPIO.HIGH)


def blue_LED_on(state):
    if state is True:
        GPIO.output(BLUE, GPIO.LOW)
    else:
        GPIO.output(BLUE, GPIO.HIGH)


def red_LED_on(state):
    if state is True:
        GPIO.output(RED, GPIO.LOW)
    else:
        GPIO.output(RED, GPIO.HIGH)


def main():
    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)

    bw_down = 0
    i = 0

    while bw_down < lower_limit:
        i += 1
        if print_messages:
            print("Bandwidth below limit or first iteration, Iteration %d" % (i))
        if i > max_iterations:
            # reset
            GPIO.output(RELAIS_1, GPIO.LOW)
            if print_messages:
                print('kill em all')
            time.sleep(5)
            GPIO.output(RELAIS_1, GPIO.HIGH)
            time.sleep(60)
            post_request({VARIABLE: 0.0, VARIABLE_2: 2.0})
            red_LED_on(False)
            break
        if print_messages:
            print("Speedtest started")
        try:
            blue_LED_on(True)

            #SIMULATE
            # bw_down = 18780752.1644
            # bw_up = 4100042.51876
            # ping = 33.941

            #TEST
            s = speedtest.Speedtest()
            s.get_best_server()
            bw_down = s.download()
            bw_up = s.upload()
            results_dict = s.results.dict()
            ping = (results_dict['ping'])

            blue_LED_on(False)
        except:
            bw_down = 0
            bw_up = 0
            ping = 0
            blue_LED_on(False)
            if print_messages:
                print("Speedtest failed")
        current_time = time.strftime("%H:%M:%S, %d.%m.%Y")
        if print_messages:
            print("Download: %d, Upload: %d, Ping: %d" % (bw_down, bw_up, ping))
        if bw_down < lower_limit:
            red_LED_on(True)
            if print_messages:
                print("try again in 60sec")
            time.sleep(60)
        else:
            red_LED_on(False)

    image = Image.new('1', (epd2in9.EPD_HEIGHT, epd2in9.EPD_WIDTH), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # write strings to the buffer
    font = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 16)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSans.ttf', 26)
    font3 = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Light.ttf', 12)
    font4 = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 10)
    font5 = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf', 23)

    draw.rectangle((20, 6, 276, 48), fill = 0)
    draw.text((26, 12), 'Bandwidth Monitor', font = font5, fill = 255)
    draw.text((210, 36), 'V0.4 by HoChri', font = font4, fill = 255)

    start_y = 53
    offset_y_1 = 19
    offset_y_2 = 27
    draw.text((6, start_y), "Ping:", font=font, fill = COLORED)
    draw.text((10, start_y + offset_y_1), ('{:5.1f}'.format(ping)), font=font2, fill = COLORED)
    draw.text((76, start_y + offset_y_2), 'ms', font=font3, fill = COLORED)

    draw.text((100, start_y), "Download:", font=font, fill=COLORED)
    draw.text((100, start_y + offset_y_1), ('{:5.2f}'.format(bw_down/1E6,2)), font=font2, fill=COLORED)
    draw.text((168, start_y + offset_y_2), 'Mbps', font=font3, fill=COLORED)

    draw.text((210, start_y), "Upload:", font=font, fill=COLORED)
    draw.text((210, start_y + offset_y_1), ('{:4.2f}'.format(bw_up/1E6,2)), font=font2, fill=COLORED)
    draw.text((264, start_y + offset_y_2), 'Mbps', font=font3, fill=COLORED)

    current_time = time.strftime("%H:%M:%S, %d.%m.%Y")
    draw.text((6, 105), 'tested @' + current_time, font=font3, fill=COLORED)


    # display the frame
    epd.Clear(0xFF)
    #epd.set_frame_memory(image.rotate(270,expand=True), 0, 0)
    epd.display(epd.getbuffer(image.rotate(270,expand=True)))
    epd.sleep()

    payload = {VARIABLE_LABEL_1: round(bw_up/1E6,2),
               VARIABLE_LABEL_2: round(bw_down/1E6,2),
               VARIABLE_LABEL_3: round(ping,2)}


    if print_messages:
        print("[INFO] Attemping to send data")
    post_request(payload)
    if print_messages:
        print("[INFO] finished")

if __name__ == '__main__':
    main()
