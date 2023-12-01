import utime
from mfrc522 import MFRC522
from dfplayermini import Player
from machine import Pin
from neopixel_pio import *

"""********************* Configuration GPIO **********************"""
#Pin OUT -> Relais
eyes	= neopixel_pio(5, 7) #Pin 0
mouth	= Pin(6, Pin.OUT)	 #Pin 2

"""*************** Communications initialization *****************"""
#UART	-> MP3
mp3 = Player(pin_TX=16, pin_RX=17)
mp3.volume(15)
#UART	-> Écran
#SPI	-> RFID
rc522 = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

"""************************** Variables **************************"""
STATE = ["BALL_IS_PRESENT", "BALL_IS_NOT_PRESENT", "BALL_IS_BACK",
         "QUIZZ","QUIZZ_TRUE","QUIZZ_FALSE"]
#RFID
BALL_UID = "[0x37, 0x89, 0x02, 0x33]"
READ_UID = ""

"""************************** Function ***************************"""
def read_uid(reader):
    PreviousCard = [0]
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        UID = reader.tohexstring(uid)
    else:
        UID=[0]
            
    return UID 
"""************************ Main program *************************"""
rc522.init()

#Vérification de la présence de la boule
READ_UID = read_uid(rc522)

#Attente si la boule n'est pas présentz
while BALL_UID != READ_UID:
    READ_UID = read_uid(rc522)

#Passage à l'état initial
actual_state = STATE[0]

while True:
    if actual_state == "BALL_IS_PRESENT":
        print("BALL_IS_PRESENT")
        #Fermeture de la bouche (Relais)
        mouth.off()
        eyes.neopixel_display(GREEN_EYES)
        
        #Vérifier la présence de la boule sur le support (RFID)
        READ_UID = read_uid(rc522)
        print(READ_UID)
        start_time = utime.ticks_ms()
        while READ_UID == BALL_UID:
            if utime.ticks_diff(utime.ticks_ms(),start_time)>=50:
                READ_UID = read_uid(rc522)
                if READ_UID != BALL_UID:
                    actual_state = STATE[1]
                else:
                    actual_state = STATE[0]
                    
        
    elif actual_state == "BALL_IS_NOT_PRESENT":
        print("BALL_IS_NOT_PRESENT")
        #Changement de la couleur des yeux
        eyes.neopixel_display(RED_EYES)
        
        #Jouer le fichier MP3
        #mp3.module_wake()
        mp3.play(3)
        utime.sleep(2) #!!!!!!!!!!!!!!!!!!!!!!!
        #mp3.fadeout(fadeout_ms)
        #mp3.module_sleep()
        
        #Attendre que la boule soit de retour (RFID)
        READ_UID = read_uid(rc522)
        start_time = utime.ticks_ms()
        while READ_UID != BALL_UID:
            if utime.ticks_diff(utime.ticks_ms(),start_time)>=50:
                start_time = utime.ticks_ms()
                READ_UID = read_uid(rc522)
                
        actual_state = STATE[2]
        
    elif actual_state == "BALL_IS_BACK":
        print("BALL_IS_BACK")
        #Changement de la couleur des yeux
        eyes.neopixel_display(YELLOW_EYES)
        utime.sleep(5)
        
        #Jouer un fichier MP3 ?????????
        
        #Attendre le start quizz (bouton HMI)
        
        actual_state = STATE[3]
        
    elif actual_state == "QUIZZ":
        print("QUIZZ")
        #Affihcher le quizz
        
        #Attendre la réponse du quizz (bouton HMI)
        # -> Si bonne réponse : state(4)
        # -> Si mauvaise réponse : state(5)
        
        actual_state = STATE[4]
        
    elif actual_state == "QUIZZ_TRUE":
        print("QUIZZ_TRUE")
        #Ouverture de la bouche (Relais)
        mouth.on()
        utime.sleep(5)
        ##Jouer un fichier MP3 ?????????
        
        #Attendre la fin de la partie (bouton HMI)
        
        actual_state = STATE[0]
        
    elif actual_state == "QUIZZ_FALSE":
        print("QUIZZ_FALSE")
        #Animation approprié
        
        #Attendre la fin de la partie (bouton HMI)
        
        actual_state = STATE[0]
