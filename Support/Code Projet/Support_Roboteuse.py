"""**********************************************************************************
Author:			Abras Frank
Creation date:	03 december 2023
Update date:	28 march 2024
Description:	Main file for the Roboteuse's support
*********************************************************************************"""
import utime
from mfrc522 import MFRC522
from dfplayermini import Player
from machine import Pin, UART
from Support_Roboteuse_util import *
from nextion_hmi import *
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
nxt = NXT_HMI(pin_TX=8, pin_RX=9)
#SPI	-> RFID
rc522 = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

"""************************** Variables **************************"""
STATE = ["STANDBY", "BALL_IS_NOT_PRESENT",
         "QUIZZ","QUIZZ_TRUE","END_OF_GAME"]
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
    """################################## FIRST STATE ###################################"""  
    if actual_state == "STANDBY":	#Initial state: ball on the holder
        mouth.off()							#Closes mouth (relay)
        eyes.neopixel_display(GREEN_EYES)
        if nxt.any():
            recv_nxt = nxt.recv()
            if recv_nxt == "LOCK":				#Locks the game during setup
                hmi_setting_up(nxt)				#Setup function
            else:
                print("données non reconnue")
        else:   
            READ_UID = read_uid(rc522)			#Checks if the ball is still on the holder
            if READ_UID != BALL_UID:			#if not, transistion to the second state
                returned = nxt_lockButton(bpParamaters)
                actual_state = STATE[1]			#Transistion to the second state
                playMP3 = True
            
        utime.sleep_ms(50)
    """################################## SECOND STATE #################################"""  
    elif actual_state == "BALL_IS_NOT_PRESENT":	#Second state: ball not on the holder
        #print("BALL_IS_NOT_PRESENT")
        eyes.neopixel_display(RED_EYES) 		#Changes eye color to red
        if playMP3 == True:						#Checks if the MP3 file should be played
            mp3.play(2)							#Plays MP3 file by index
            utime.sleep(3)
            playMP3 = False						#Allows you to play the file only once 
        
        READ_UID = read_uid(rc522)				#Wait until the ball is back on the holder
        if READ_UID == BALL_UID:				#if it's true, transistion to the third state
            actual_state = STATE[2]				#Transistion to the third state
            
        utime.sleep_ms(50)
    """################################## THIRD STATE #################################"""  
    elif actual_state == "QUIZZ":
        #print("BALL_IS_BACK")
        eyes.neopixel_display(YELLOW_EYES)		#Changes eye color to yellow
        quizz = quizz_generator()
        display_quizz(quizz)
        
        while nxt.any() <= 0:
            pass
        else:
            choice = nxt.recv()
            if choice == quizz[4]:
                actual_state = STATE[3]
            else:
                actual_state = STATE[4]
        
        utime.sleep_ms(50)													
        
        actual_state = STATE[3]					#Transistion to the fourth state
    """################################# FOURTH STATE #################################"""  
    elif actual_state == "QUIZZ_TRUE":
        #print("QUIZZ_TRUE")
        eyes.neopixel_display(LIGHT_OFF)
        utime.sleep(2)
        eyes.neopixel_display(GREEN_EYES)
        
        mouth.on()								#Opens mouth (relay)
        utime.sleep(3)
        
        actual_state = STATE[4]					#Transistion to the fifth state
    """################################## FIFTH STATE #################################"""   
    elif actual_state == "END_OF_GAME":
        #print("QUIZZ_FALSE")
        while nxt.any() <= 0:
            pass
        else:
            recv_nxt = nxt.recv()
            if recv_nxt == "endgame":
                actual_state = STATE[0]			#Transistion to the initial state
