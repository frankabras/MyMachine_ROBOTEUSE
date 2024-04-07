from machine import Pin, UART

#End-of-query characters (from Nextion request)
endChar = "\xFF"

""" Tools' reference on the HMI (Commanded by RPI)"""
#Pages names
p0 = "MainMenu"
p1 = "Parameters"
p2 = "NewQuestion"
p3 = "Quizz"
#Page 0 - MainMenu
bpParamaters = "b00"
dispText = "t04"
#Page 3 - Quizz
dispQuestion = "t30"
dispOption1 = "b30"
dispOption2 = "b31"
dispOption3 = "b32"

""" Colors set (same of nextion project)"""
NXT_BLACK 		= 0
NXT_WHITE 		= 65_535
NXT_LIGHT_BLUE	= 53_055
NXT_BLUE 		= 26_015
NXT_GREEN 		= 25_985
NXT_RED 		= 64_235

""" Functions to conntrol HMI """
class NXT_HMI:
    def __init__(self,pin_TX,pin_RX):
        self.NXT = UART(1, 9600, tx=Pin(int(pin_TX)), rx=Pin(int(pin_RX)))
        
    def recv(self):
        while self.NXT.any():
            recv_char = self.NXT.read(1)				#Reads one byte
            recv_data += recv_char						#Adds new byte to those already received
            if endChar in recv_data.decode('utf-8'):	#If end character received
                recv_data = recv_data.decode('utf-8')		#Decodes data
                recv_data = recv_data.split(endChar)			#Removes end character
                recv_nxt = recv_data[0]						#Copies data
            
        return recv_nxt
                
    def changePage(self,PageName):
        toSend = "page " + PageName
        self.NXT.write(toSend.encode('utf-8'))
    
    def changeTXT(self,toolRef,newTxt):
        newTxt = "\"" + newTxt + "\""
        toSend = toolRef + ".txt=" + newTxt
        self.NXT.write(toSend.encode('utf-8'))
    
    def changeBCO(self,toolRef,color): #Background color
        color = str(color)
        toSend = toolRef + ".bco=" + color
        self.NXT.write(toSend.encode('utf-8'))
    
    def changePCO(self,toolRef,color): #Police color
        color = str(color)
        toSend = toolRef + ".pco=" + color
        self.NXT.write(toSend.encode('utf-8'))
    
    def lockButton(self,toolRef):
        toSend = "tsw " + toolRef + ",0"
        self.NXT.write(toSend.encode('utf-8'))

    def unlockButton(self,toolRef):
        toSend = "tsw " + toolRef + ",1"
        self.NXT.write(toSend.encode('utf-8'))

