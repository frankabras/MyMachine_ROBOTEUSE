"""**********************************************************************************
Author:			Abras Frank
Creation date:	03 december 2023
Update :		20 april 2024
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
eyes = neopixel_pio(5, 7)
eyes.neopixel_display(LIGHT_OFF)
#Relais
openMouth = Pin(6, Pin.OUT)
closeMouth = Pin(7, Pin.OUT)
openMouth.off()
closeMouth.on()

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
         "QUIZZ","GOOD","BAD","END_OF_GAME"]
#RFID
BALL_UID = "[0x37, 0x89, 0x02, 0x33]" #[0xEB, 0xC8, 0x50, 0x3E]
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
nxt.changePage(p0)
nxt.autoSleep_enable(30)

#Main loop
while True:
    if actual_state == "STANDBY":	#Initial state: ball on the holder
        print("Standby")
        openMouth.off()
        closeMouth.on()						#Closes mouth (relais)
        eyes.neopixel_display(GREEN_EYES)
        if nxt.NXT.any():
            recv_nxt = nxt.recv()
            if recv_nxt == "LOCK":				#Locks the game during setup
                hmi_setting_up(nxt,mp3)			#Setup function
            else:
                print("données non reconnue")
        else:   
            READ_UID = read_uid(rc522)			#Checks if the ball is still on the holder
            if READ_UID != BALL_UID:			#if not, transistion to the second state
                nxt.autoSleep_disable()			#Lock auto-sleep during the game
                nxt.lockButton(bpParamaters)	#Lock others functions (on HMI)
                actual_state = STATE[1]			#Transistion to the second state
                playMP3 = True					
            
        utime.sleep_ms(50) 
    elif actual_state == "BALL_IS_NOT_PRESENT":	#Second state: ball not on the holder
        print("Waiting")
        eyes.neopixel_display(RED_EYES) 		#Changes eye color to red
        if playMP3 == True:						#Checks if the MP3 file should be played
            mp3.play(2)							#Plays MP3 file by index
            utime.sleep(3)
            playMP3 = False						#Allows you to play the file only once 
        
        READ_UID = read_uid(rc522)				#Wait until the ball is back on the holder
        if READ_UID == BALL_UID:				#if it's true, transistion to the third state
            actual_state = STATE[2]				#Transistion to the third state
            
        utime.sleep_ms(50) 
    elif actual_state == "QUIZZ":
        print("Quizz")
        #print("BALL_IS_BACK")
        eyes.neopixel_display(ORANGE_EYES)	#Changes eye color to yellow
        quizz = quizz_generator()				
        nxt.changePage(p3)				#Display quizz page
        display_quizz(nxt,quizz)		#Display quizz (question and options)
        
        while nxt.NXT.any() <= 0:		#Waits for answer
            continue
        
        choice = nxt.recv()					
        print(choice)
        print(quizz[4])
            
        if (quizz[4]==choice):		#Check answer (received)
            actual_state = STATE[3] #State 3 = good answer           
        else:
            actual_state = STATE[4] #State 4 = bad answer
            
    elif actual_state == "GOOD":
        print("Good")
        nxt.changeTXT(dispResult,"Bonne reponse")	#Displays the result on the HMI 
        nxt.changeBCO(dispResult,NXT_LIGHT_GREEN)	#Changes background color
        openMouth.on()
        closeMouth.off()							#Opens mouth (relais)
        eyes.neopixel_display(GREEN_EYES)			#Changes eyes' color       
        
        actual_state = STATE[5]					#Transistion to the fifth state
    elif actual_state == "BAD":
        print("Bad")
        nxt.changeTXT(dispResult,"Mauvaise reponse")	#Displays the result on the HMI 
        nxt.changeBCO(dispResult,NXT_RED)				#Changes background color
        eyes.neopixel_display(YELLOW_EYES)				#Changes eyes' color        
        
        actual_state = STATE[5]					#Transistion to the fifth state  
    elif actual_state == "END_OF_GAME":
        print("The end")
        while nxt.NXT.any() <= 0:
            continue
        else:
            recv_nxt = nxt.recv()
            utime.sleep_ms(50)
            if recv_nxt == "endgame":
                nxt.changePage(p0)				#Return to main menu
                nxt.unlockButton(bpParamaters)	#Unlock others functions (on HMI)				
                nxt.autoSleep_enable(30)		#Enable auto-sleep (delay = 30s)
                actual_state = STATE[0]			#Transistion to the initial state