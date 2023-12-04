from machine import Pin, UART
# Code pour tester la réaction de la boule lorsqu'on la met en marche
from servo_util import *

BT = UART(1,baudrate=9600, tx=Pin(4), rx=Pin(5))
servo = servomoteur(0)
led = Pin(25, Pin.OUT)

while(True):
    if BT.any():
        message = BT.readline().decode('utf-8')
        print(message)
        if (message[0]=='f'):
            led.value(1) # on allume
        if (message[0]=='b'):
            led.value(1) # on allume
        if (message[0]=='s'):
            led.value(0) # on éteint
        if (message[0]=='l'):
            servo.moveTo(0)
        if (message[0]=='r'):
            servo.moveTo(180)
        