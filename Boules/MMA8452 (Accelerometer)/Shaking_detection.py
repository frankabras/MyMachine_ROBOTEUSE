import time
from machine import Pin, I2C
from micropython_mma8452q import mma8452q

led = Pin(25, Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1))  # Correct I2C pins for RP2040
mma = mma8452q.MMA8452Q(i2c)

z_init = 10.0
z_seuil = 7.5
nb_pulse = 0

try:
    n = 1
    while True:
        x, y, z = mma.acceleration
        print(f"Acceleration: X={x:0.1f}m/s^2 y={y:0.1f}m/s^2 z={z:0.1f}m/s^2")
        print()
        
        if abs(z - z_init) >= z_seuil:
            nb_pulse = nb_pulse+1
        else:
            if nb_pulse >= 4:
                led.value(1)
                time.sleep(0.5)
                led.value(0)
            nb_pulse = 0
 
        time.sleep(0.2)
        n=n+1
except KeyboardInterrupt:
    print("End of program")

