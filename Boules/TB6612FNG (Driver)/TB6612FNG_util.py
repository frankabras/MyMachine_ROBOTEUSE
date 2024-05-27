from machine import Pin , PWM
from utime import sleep

PWM_FREQUENCY = 1000

class bimotors_driver:
    def __init__(self, pin_inA1, pin_inA2, pin_pwmA, pin_inB1, pin_inB2, pin_pwmB):
        #Motor A
        self.MotorA_1 = Pin(int(pin_inA1),Pin.OUT)
        self.MotorA_2 = Pin(int(pin_inA2),Pin.OUT)
        self.MotorA_pwm = PWM(Pin(int(pin_pwmA)))
        self.MotorA_pwm.freq(PWM_FREQUENCY)
        #Motor B
        self.MotorB_1 = Pin(int(pin_inB1),Pin.OUT)
        self.MotorB_2 = Pin(int(pin_inB2),Pin.OUT)
        self.MotorB_pwm = PWM(Pin(int(pin_pwmB)))
        self.MotorB_pwm.freq(PWM_FREQUENCY)

    #
    def stop_rotate(self, motor="All"):
        if motor == "A" or "All":
            self.MotorA_1.value(0)
            self.MotorA_2.value(0)
            self.MotorA_pwm.duty_u16(0)
        if motor == "B" or "All":
            self.MotorB_1.value(0)
            self.MotorB_2.value(0)
            self.MotorB_pwm.duty_u16(0)

    #
    def rotate_cw(self, motor="All", speed=65535):
        if motor == "MotorA" or "All":
            self.MotorA_1.value(1)
            self.MotorA_2.value(0)
            self.MotorA_pwm.duty_u16(speed)
        if motor == "MotorB" or "All":
            self.MotorB_1.value(1)
            self.MotorB_2.value(0)
            self.MotorB_pwm.duty_u16(speed)
        else: 
            print("ERROR : BAD MOTOR INDICATION")
        
    #
    def rotate_ccw(self, motor="All", speed=65535):
        if motor == "A" or "All":
            self.MotorA_1.value(0)
            self.MotorA_2.value(1)
            self.MotorA_pwm.duty_u16(speed)
        if motor == "B" or "All":
            self.MotorB_1.value(0)
            self.MotorB_2.value(1)
            self.MotorB_pwm.duty_u16(speed) 

    #
    def set_speed(self, motor="All", speed=65535):
        if motor == "A" or "All":
            self.MotorA_pwm.duty_u16(speed)
        if motor == "B" or "All":
            self.MotorB_pwm.duty_u16(speed)

if __name__ == "__main__":
    # execute only if run as the main module (i.e. not an import module)
    driver = bimotors_driver(8, 7, 6, 10, 11, 12)

    try:
        while True :
            driver.rotate_cw(speed=32000)
            sleep(5)
            driver.stop_rotate()
            sleep(1)
            driver.rotate_ccw(speed=65000)
            sleep(5)
            driver.stop_rotate()
            sleep(1)
    except KeyboardInterrupt:
        print("End of program")