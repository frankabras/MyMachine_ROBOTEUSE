import utime
from mfrc522 import MFRC522
from dfplayermini import Player
from machine import Pin
from Support_Roboteuse_util import *
from neopixel_pio import *

"""********************* Configuration GPIO **********************"""
#Neopixels
eyes	= neopixel_pio(5, 7)
eyes.neopixel_display(LIGHT_OFF)
#Relais
mouth	= Pin(6, Pin.OUT)
mouth.off()

"""*************** Communications initialization *****************"""
#UART	-> MP3
mp3 = Player(pin_TX=16, pin_RX=17)
mp3.module_reset()
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
ballPresence = False


"""************************ Main program *************************"""
#Wait until the ball is on the holder
READ_UID = read_uid(rc522)
while BALL_UID != READ_UID:
    READ_UID = read_uid(rc522)
    utime.sleep_ms(50)

#Transition to the initial state
actual_state = STATE[0]

#Main loop
while True:
    if actual_state == "BALL_IS_PRESENT":	#Initial state: ball on the holder
        print("BALL_IS_PRESENT")
        mouth.off()							#Closes mouth (relay)
        eyes.neopixel_display(GREEN_EYES)	#Changes eye color to green
        
        READ_UID = read_uid(rc522)			#Checks if the ball is still on the holder
        if READ_UID != BALL_UID:			#if not, transistion to the second state
            actual_state = STATE[1]
            playMP3 = True
            
        utime.sleep_ms(50)
        
    elif actual_state == "BALL_IS_NOT_PRESENT":	#Second state: ball not on the holder
        print("BALL_IS_NOT_PRESENT")
        eyes.neopixel_display(RED_EYES) 		#Changes eye color to red
        
        if playMP3 == True:						#Checks if the MP3 file should be played
            mp3.play(1)							#Plays MP3 file by index
            utime.sleep(3)
            playMP3 = False						#Allows you to play the file only once 
        
        READ_UID = read_uid(rc522)				#Wait until the ball is back on the holder
        if READ_UID == BALL_UID:				#if it's true, transistion to the third state
            actual_state = STATE[2]
            
        utime.sleep_ms(50)
        
    elif actual_state == "BALL_IS_BACK":
        print("BALL_IS_BACK")
        eyes.neopixel_display(YELLOW_EYES)		#Changes eye color to yellow
        
        #CODE TO BE COMPLETED (Screen)
        utime.sleep(5)													
        
        actual_state = STATE[3]					#Transistion to the fourth state
        
    elif actual_state == "QUIZZ":
        print("QUIZZ")
        
        #CODE TO BE COMPLETED (Display Quizz)
        
        #Wait answer of yhe Quizz 
        # -> If good answer : Transistion to the fifth state
        # -> If bad answer : Transistion to the sixth state
        
        actual_state = STATE[4]					#Transistion to the fifth state
        
    elif actual_state == "QUIZZ_TRUE":
        print("QUIZZ_TRUE")
        mouth.on()								#Opens mouth (relay)
        
        #CODE TO BE COMPLETED (End of game - Screen)
        utime.sleep(5)
        
        actual_state = STATE[0]					#Transistion to the initial state
        
    elif actual_state == "QUIZZ_FALSE":
        print("QUIZZ_FALSE")
        
        #CODE TO BE COMPLETED
        
        actual_state = STATE[0]					#Transistion to the initial state
