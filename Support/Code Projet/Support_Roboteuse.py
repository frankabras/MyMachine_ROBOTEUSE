import utime
from machine import Pin
from neopixel_pio import *

"""********************* Configuration GPIO **********************"""
#Pin OUT -> Relais
eyes	= neopixel_pio(0, 7) #Pin 0
mouth	= Pin(3, Pin.OUT)	 #Pin 2

"""*************** Communications initialization *****************"""
#UART	-> MP3
#UART	-> Écran
#SPI	-> RFID

"""************************** Variables **************************"""
state = ["BALL_IS_PRESENT", "BALL_IS_NOT_PRESENT", "BALL_IS_BACK",
         "QUIZZ","QUIZZ_TRUE","QUIZZ_FALSE"]
BALL_UID = "[0x37, 0x89, 0x02, 0x33]"

"""************************** Function ***************************"""


"""************************ Main program *************************"""
#Vérifier si la boule est présente (RFID)
# -> Si oui : state[0]
# -> Si non : attendre que la boule soit déposée sur le support pour commmencer
actual_state = state[1]

if actual_state == "BALL_IS_PRESENT":
    print("BALL_IS_PRESENT")
    mouth.off()
    #Vérifier la présence de la boule sur le support (RFID)
    
elif actual_state == "BALL_IS_NOT_PRESENT":
    print("BALL_IS_NOT_PRESENT")
    eyes.neopixel_display(RED_LIST)
    #Jouer le fichier MP3
    #Attendre que la boule soit de retour (RFID)
    
elif actual_state == "BALL_IS_BACK":
    print("BALL_IS_BACK")
    eyes.neopixel_display(BLUE_LIST)
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
    mouth.on()
    #Ouverture de la bouche
    # "Jouer le fichier MP3 approprié"
    #Attendre la fin de la partie (bouton HMI)
    
elif actual_state == "QUIZZ_FALSE":
    print("QUIZZ_FALSE")
    #Animation approprié
    #Attendre la fin de la partie (bouton HMI)
    