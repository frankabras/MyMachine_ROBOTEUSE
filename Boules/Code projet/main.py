"""
Code
"""
import utime
from random import *
from machine import Pin, UART, I2C, Timer
from TB6612FNG_util import *
from servo_util import *
from micropython_mma8452q import mma8452q

#Variables
run_mode = False
RIGHT = 0
MIDDLE_RIGHT = 45
GO_STRAINGHT = 90
MIDDLE_LEFT = 135
LEFT = 180
random_motion = [RIGHT,MIDDLE_RIGHT,GO_STRAINGHT,MIDDLE_LEFT,LEFT]
random_delay = 1000
z_init =-10.0
z_seuil = 5
nb_pulse = 0

#Devices
led = Pin(25, Pin.OUT)
led.value(0)
servo = servomoteur(14)
servo.moveTo(GO_STRAINGHT)
driver = bimotors_driver(7, 8, 6, 10, 11, 12)
driver.stop_rotate()
i2c = I2C(1, sda=Pin(2), scl=Pin(3))
mma = mma8452q.MMA8452Q(i2c)

try:
    while True:
        #Lecture des données de l'accéléromètre
        x, y, z = mma.acceleration
        print(f"Acceleration: X={x:0.1f}m/s^2 y={y:0.1f}m/s^2 z={z:0.1f}m/s^2")
        print()
        
        #Vérification des valeurs de l'accéléromètre
        if abs(z - z_init) >= z_seuil:
            nb_pulse = nb_pulse+1
            if nb_pulse >= 3:
                if run_mode == False:
                    led.value(1)
                    driver.rotate_cw()
                    run_mode = True
                    start_time=utime.ticks_ms()
                    random_delay = 1000
                else:
                    led.value(0)
                    run_mode = False
        else:
            nb_pulse = 0
        
        #Contrôle du mouvement de la boule
        if run_mode == True:
            if utime.ticks_diff(utime.ticks_ms(),start_time)>=random_delay:
                motion = randint(1,4)
                servo.moveTo(random_motion[motion])
                random_delay = randint(1000,5000)
                start_time=utime.ticks_ms()
        else:
            driver.stop_rotate()
            servo.moveTo(GO_STRAINGHT)
 
        utime.sleep(0.2)
except KeyboardInterrupt:
        print("End of program")