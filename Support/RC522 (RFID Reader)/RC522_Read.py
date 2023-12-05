from mfrc522 import MFRC522
import utime
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
my_UID = "[0x37, 0x89, 0x02, 0x33]"

print("")
print("Place card into reader")
print("")

PreviousCard = [0]

try:
    while True:

        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue

            if stat == reader.OK:
                UID = reader.tohexstring(uid)
                print(UID)
                if UID == my_UID:
                    print("OK")
                PreviousCard = uid
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    print("Bye")