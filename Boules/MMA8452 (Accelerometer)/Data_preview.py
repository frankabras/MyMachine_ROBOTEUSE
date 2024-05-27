import time
import uos
from machine import Pin, I2C
from micropython_mma8452q import mma8452q, i2c_helpers

file = "acc_data.csv"

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mma = mma8452q.MMA8452Q(i2c)

f = open(file, "w") # "w" overwrire file, "a" append to file
f.write("measure;x_val;y_val;z_val\r\n") # header

try:
    n = 1
    while n < 26:
        x, y, z = mma.acceleration
        print(f"Acceleration: X={x:0.1f}m/s^2 y={y:0.1f}m/s^2 z={z:0.1f}m/s^2")
        print()
        
        dataToCSV = [n,x,y,z]
        buffer="%d;%1.1f;%1.1f;%1.1f\r\n"%(dataToCSV[0],dataToCSV[1],dataToCSV[2],dataToCSV[3]) 
        f.write(buffer)
        
        time.sleep(0.2)
        n=n+1
except KeyboardInterrupt:
    print("End of program")
    
f.close()
 
fsys_info = uos.statvfs('/')    # 
freeSize=fsys_info[3]           # number of remaining free blocks after adding data
                                # for Raspberry Pi Pico a block is 4096 bytes
print("Number of free blocks", freeSize)