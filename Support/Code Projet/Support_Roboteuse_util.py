"""**********************************************************************************
Author:			Abras Frank
Creation date:	03 december 2023
Update date:	03 december 2023
Description:	File with the functions usefull for the Support_Roboteuse.py program
*********************************************************************************"""

"""***************************** RFID Function **********************************"""
# Description : Used to read an RFID tag and to return its UID
# IN:	reader - mfrc522 object used for RC552 interfacing
# OUT:	UID - UID of tag in str format
def read_uid(reader):
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            UID = reader.tohexstring(uid)
    else:
        UID=[None]
            
    return UID 