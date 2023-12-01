from machine import Pin , PWM
from utime import sleep

#Moteur 1
ina1 = Pin(10,Pin.OUT)
ina2 = Pin(11, Pin.OUT)
pwma = PWM(Pin(12))
#Moteur 2
inb1 = Pin(20,Pin.OUT)
inb2 = Pin(21, Pin.OUT)
pwmb = PWM(Pin(22))

pwma.freq(1000)
pwmb.freq(1000)

def RotateCW(duty):
    duty_16 = int((duty*65536)/100)
    #Moteur 1
    ina1.value(1)
    ina2.value(0)
    pwma.duty_u16(duty_16)
    #Moteur 2
    inb1.value(1)
    inb2.value(0)
    pwmb.duty_u16(duty_16)

def RotateCCW(duty):
    duty_16 = int((duty*65536)/100)
    #Moteur 1
    ina1.value(0)
    ina2.value(1)
    pwma.duty_u16(duty_16)
    #Moteur 2
    inb1.value(0)
    inb2.value(1)
    pwmb.duty_u16(duty_16)
    
def StopMotor():
    #Moteur 1
    ina1.value(0)
    ina2.value(0)
    pwma.duty_u16(0)
    #Moteur 2
    inb1.value(0)
    inb2.value(0)
    pwmb.duty_u16(0)

while True:
    duty_cycle=float(input("Enter pwm duty cycle"))
    print (duty_cycle)
    RotateCW(duty_cycle)
    sleep(5)
    RotateCCW(duty_cycle)
    sleep(5)
    StopMotor()
