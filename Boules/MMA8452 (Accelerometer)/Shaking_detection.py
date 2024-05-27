import time
from machine import Pin, I2C
from micropython_mma8452q import mma8452q

led = Pin(25, Pin.OUT)
i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mma = mma8452q.MMA8452Q(i2c)

z_init =-10.0
z_seuil = 6.5
y_seuil = 10.0
x_seuil = 10.0
nb_pulse = 0

try:
    while True:
        x, y, z = mma.acceleration
        print(f"Acceleration: X={x:0.1f}m/s^2 y={y:0.1f}m/s^2 z={z:0.1f}m/s^2")
        print()
        
        if abs(z - z_init) >= z_seuil:
            nb_pulse = nb_pulse+1
            if nb_pulse >= 3:
                led.value(1)
                time.sleep(0.5)
                led.value(0)
        else:
            nb_pulse = 0
        
        if abs(y) >= y_seuil or abs(x) >= x_seuil:
            led.value(1)
            time.sleep(0.5)
            led.value(0)
            time.sleep(0.5)
            led.value(1)
            time.sleep(0.5)
            led.value(0)
        
 
        time.sleep(0.2)
except KeyboardInterrupt:
    print("End of program")

