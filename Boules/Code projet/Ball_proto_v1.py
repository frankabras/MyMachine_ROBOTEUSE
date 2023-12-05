"""
Code pour tester la réaction de la boule lorsqu'on la met en marche
"""
from machine import Pin, UART
from servo_util import *

BT = UART(1,baudrate=9600, tx=Pin(4), rx=Pin(5))
servo = servomoteur(0)
driver = bimotors_driver(10, 11, 12, 20, 21, 22)

try:
    while True:
        if BT.any():
            message = BT.readline().decode('utf-8')
            print(message)
            if (message[0]=='f'):
                driver.rotate_cw()
            if (message[0]=='b'):
                driver.rotate_ccw()
            if (message[0]=='s'):
                driver.stop_rotate()
            if (message[0]=='l'):
                servo.moveTo(0)
            if (message[0]=='r'):
                servo.moveTo(180)
except KeyboardInterrupt:
        print("End of program")