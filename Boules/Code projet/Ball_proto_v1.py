"""
Code pour tester la réaction de la boule lorsqu'on la met en marche
"""
from machine import Pin, UART
from TB6612FNG_util import *
from servo_util import *

BT = UART(0,baudrate=9600, tx=Pin(16), rx=Pin(17))
servo = servomoteur(14)
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
                servo.moveTo(90)
            if (message[0]=='l'):
                servo.moveTo(0)
            if (message[0]=='r'):
                servo.moveTo(180)
except KeyboardInterrupt:
        print("End of program")