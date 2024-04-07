"""**********************************************************************************
Author:			Abras Frank
Creation date:	03 december 2023
Update date:	01 march 2024
Description:	File with the functions usefull for the Support_Roboteuse.py program
*********************************************************************************"""
from random import *
import ujson as json
from nextion_hmi import *

questions_file = "/questions.json"
"""***************************** RFID Function **********************************"""
# Description : Used to read an RFID tag and to return its UID
# IN:	reader - mfrc522 object used for RC552 interfacing
# OUT:	UID - UID of tag in str format
def read_uid(reader):
    reader.init()
    UID=[None]
    
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            UID = reader.tohexstring(uid)
            
    return UID

"""*********************** UART function for nextion ****************************"""
def save_new_question(data):
    #Data slicing
    data = data.split("+")

    #Putting the data in json file format
    question = [
    {
        "question": str(data[0]),
        "options": [str(data[1]),str(data[2]),str(data[3])],
        "answer": str(data[4])
    }]
    
    #Saving new question in json file
    with open(questions_file, "w") as file:
        json.dump(questions, file)

def hmi_setting_up(nxt,player):
    recv = ""
    while recv != "UNLOCK":
        if nxt.any():
            recv = nxt.recv()
            if recv == "test_volume":		#Code to test volume
                player.play(2)
                utime.sleep(3)
            elif recv.find("volume_") > 0:	#Code to set volume
                data = recv.split("_")
                player.volume(int(data[1]))
            elif recv == "newquestion":		#Code to add new question
                while nxt.any() <= 0:
                    pass
                else:
                    recv=nxt.recv()
                    if recv == "cancel":	#Cancel request
                        continue
                    else:
                        save_new_question(recv)
                    
def display_quizz(quizz_data):
    changeTXT(dispQuestion,quizz_data[0])	#To display question
    changeTXT(dispOption1,quizz_data[1])	#To display option n°1
    changeTXT(dispOption2,quizz_data[2])	#To display option n°2
    changeTXT(dispOption3,quizz_data[3])	#To display option n°3
    


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
        operation = str(n1)+" x "+str(n2)+" = ?"
        result = n1*n2
    else:                   #Division
        operation = str(n1)+" / "+str(n2)+" = ?"
        result = n1/n2

    
    return operation, result

def quizz_generator():
    typeOfQuestion = random()
    if typeOfQuestion <= 0.30:
        #Generates 2 random numbers between 1 and 10
        n1 = randint(1,10)
        n2 = randint(1,10)

        #If division is possible
        if n1 % n2 == 0:
            mult_or_div = randint(0,1)  #Randomly choose multiplication or division
        else:
            mult_or_div = 0 #Otherwise, multiply by default

        
        if mult_or_div == 0:    #Multiplication 
            operation = str(n1)+" x "+str(n2)+" = ?"
            result = n1*n2
        else:                   #Division
            operation = str(n1)+" / "+str(n2)+" = ?"
            result = n1/n2
        
        #Data returned within the defined format
        data = operation,str(result),str(randint(1,100)),str(randint(1,100)),str(result)
        return data
    else:
        with open(questions_file, "r") as file:
            questions = json.load(file) 		#Opening json files with the questions
            random_question = choice(questions)	#Selecting a random question
        
        #Data returned within the defined format
        data = random_question["question"],random_question["options"][0],\
               random_question["options"][1],random_question["options"][2],random_question["answer"]
        return data  
