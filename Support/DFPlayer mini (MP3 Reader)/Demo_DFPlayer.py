from dfplayermini import Player
from time import sleep

mp3 = Player(pin_TX=17, pin_RX=16)

print("set volume")
mp3.volume(10)

print("start play")
mp3.play(1)
sleep(2)

print("stop play with fadeout")
mp3.fadeout(2000)

mp3.play('next')
sleep(10)

mp3.pause()
sleep(3)

mp3.loop()
mp3.play(2)
sleep(20)

mp3.module_sleep()