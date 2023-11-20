from mfrc522 import MFRC522
import utime

# initialize RFID object
reader = MFRC522(spi_id=0,sck=18,miso=16,mosi=19,cs=17,rst=0)
print("Hold a tag near the reader")

# define parameters for acessing tag
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
PreviousCard = [0]

while True:
    # start commuication with RFID reader
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    # check if a tag can be read
    if stat == reader.OK:
        # read tag
        (stat, uid) = reader.SelectTagSN()
        # check if tag is the same as before
        if uid == PreviousCard:
            continue
        
        # check if reading went well
        if stat == reader.OK:
            #print base information about tag
            print("Card detected {} uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
            print()
            # print all blocks of the tag
            print("Read from tag:")
            reader.MFRC522_DumpClassic1K(uid, Start=0, End=64, keyA=key)
            print()

            PreviousCard = uid
            
    else:
        # reset already read tag
        PreviousCard=[0]

utime.sleep_ms(50)