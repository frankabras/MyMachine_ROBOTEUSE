"""**********************************************************************************
Author:			Abras Frank
Creation date:	03 december 2023
Update date:	03 december 2023
Description:	File with the functions usefull for the Support_Roboteuse.py program
*********************************************************************************"""
from random import *

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

"""********************************** QUIZZ *************************************"""
def quizz_math():
    #Generates 2 random numbers between 1 and 10
    n1 = randint(1,10)
    n2 = randint(1,10)

    #If division is possible
    if n1 % n2 == 0:
        mult_or_div = randint(0,1)  #Randomly choose multiplication or division
    else:
        mult_or_div = 0 #Otherwise, multiply by default

    
    if mult_or_div == 0:    #Multiplication 
        operation = "%dx%d" % n1, n2  
        print(n1,"x",n2,"= ?")
        result = n1*n2
    else:                   #Division
        operation = "%d/%d" % n1, n2 
        result = n1/n2

    
    return operation, result