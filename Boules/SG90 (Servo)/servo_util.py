"""
AUTHOR  : ABRAS Frank
LIBRARY : SERVOMOTOR CONTROL
NB      : Developped and tested on SG90 
            frequency : 50Hz
            position : 0 to 180°
"""
from machine import Pin,PWM

# PWM values
MIN_PWM = 1750                              # 0°
MAX_PWM = 8450                              # 180°
MID_PWM = int(MIN_PWM+(MAX_PWM-MIN_PWM)/2)  # 90°
# Angles values
MIN_ANGLE = 0                               
MAX_ANGLE = 180
# Constant
U16_PER_DEGREE = 37.2                       # (MAX_PW-MIN_PWM)/MAX_ANGLE
PWM_FREQUENCY = 50                          # Frenquency of SG90

class servomoteur:
    def __init__(self, pin):
        self.servo = PWM(Pin(int(pin), mode=Pin.OUT))
        self.servo.freq(PWM_FREQUENCY)

        self.servo.duty_u16(MID_PWM)
    
    def moveTo(self, position):
        self.pwm_value = int(1750+(37.2*position))

        if self.pwm_value > MAX_PWM:
            self.pwm_value = MAX_PWM
        elif self.pwm_value < MIN_PWM:
            self.pwm_value = MIN_PWM
        
        self.servo.duty_u16(self.pwm_value)


if __name__ == "__main__":
    # execute only if run as the main module (i.e. not an import module)
    servo = servomoteur(0)
    position = int(input("Enter position of servo (0 to 180°) : "))

    while position != 999:
        servo.moveTo(position)
        position = int(input("Enter position of servo (0 to 180°) : "))