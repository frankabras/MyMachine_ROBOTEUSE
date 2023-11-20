import utime
from machine import Pin

"""********************* Configuration GPIO **********************"""
relay = Pin(2, Pin.OUT)

print("Menu :")
print("	Pour ouvrir : open")
print("	Pour fermer : close")
print("	Pour quitter : exit")
print("---------------------")

cmd = input("Choisir une option : ")
while cmd != "exit":
    if cmd == "close":
        relay.off()
    elif cmd == "open":
        relay.on()
    else:
        print("commande invalide")
        
    cmd = input("Choisir une option : ")
    
print("Menu quitté")