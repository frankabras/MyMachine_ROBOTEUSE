# programme non testé !!
# pour Sharp GP2YA41SK0F
from machine import ADC, Pin
from time import *


can = ADC(Pin(34))               # crée un objet ADC sur la broche 34
can.atten(ADC.ATTN_11DB)         # étendue totale : 3.3V
ADC.width(ADC.WIDTH_10BIT)       # change la résolution du convertisseur à 10bits

while True:
    Ncan = can.read()                    # conversion analogique-numérique broche P0  0-1023
    dist_cm = 1092.2 * pow(Ncan, -0.853)
    print ('Distance en cm = ', dist_cm)     # affichage sur la console de la valeur numérique 

    sleep_ms(500)