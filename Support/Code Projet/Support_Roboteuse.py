import utime
from machine import Pin
from neopixel_pio import *

"""********************* Configuration GPIO **********************"""
#Pin OUT -> Relais
left_eye	= neopixel_pio(0, 4) #Pin 0
right_eye	= neopixel_pio(1, 4) #Pin 1
relay		= Pin(2, Pin.OUT)	 #Pin 2

"""*************** Communications initialization *****************"""
#UART	-> MP3
#UART	-> Écran
#SPI	-> RFID

"""************************** Variables **************************"""
state = ["BALL_IS_PRESENT", "BALL_IS_NOT_PRESENT", "BALL_IS_BACK",
         "QUIZZ","QUIZZ_TRUE","QUIZZ_FALSE"]


"""************************ Main program *************************"""
#Vérifier si la boule est présente (RFID)
# -> Si oui : state[0]
# -> Si non : attendre que la boule soit déposée sur le support pour commmencer
actual_state = state[0]

if actual_state == "BALL_IS_PRESENT":
    print("BALL_IS_PRESENT")
    #Vérifier la présence de la boule sur le support (RFID)
    
elif actual_state == "BALL_IS_NOT_PRESENT":
    print("BALL_IS_NOT_PRESENT")
    left_eye.neopixel_display(RED_LIST)
    right_eye.neopixel_display(RED_LIST)
    #Jouer le fichier MP3
    #Attendre que la boule soit de retour (RFID)
    
elif actual_state == "BALL_IS_BACK":
    print("BALL_IS_BACK")
    left_eye.neopixel_display(BLUE_LIST)
    right_eye.neopixel_display(BLUE_LIST)
    # "Jouer le fichier MP3 approprié"
    #Attendre le start quizz (bouton HMI)
elif actual_state == "QUIZZ":
    print("QUIZZ")
    #Affihcher le quizz
    #Attendre la réponse du quizz (bouton HMI)
    # -> Si bonne réponse : state(4)
    # -> Si mauvaise réponse : state(5)
    
elif actual_state == "QUIZZ_TRUE":
    print("QUIZZ_TRUE")
    #Ouverture de la bouche
    # "Jouer le fichier MP3 approprié"
    #Attendre la fin de la partie (bouton HMI)
    
elif actual_state == "QUIZZ_FALSE":
    print("QUIZZ_FALSE")
    #Animation approprié
    #Attendre la fin de la partie (bouton HMI)
    