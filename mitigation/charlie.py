from unetpy import UnetSocket, Services
from myInfo import printNodeInformation
from datetime import datetime
from time import sleep
import string

all_letters = string.digits + string.ascii_letters + string.punctuation
s = UnetSocket('localhost',1104)
wait = 1

def makeAuthRequest(location):
    dict1 = {}
    key = 4
   
    for i in range(len(all_letters)):
        dict1[all_letters[i]] = all_letters[(i+key)%len(all_letters)]  

    cipher_txt=[]
    location = " ".join(map(str,location))
    print("Node Location : ",location)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Timestamp : ",timestamp)
    plain_txt = location + "|" + timestamp
    print("Plain Text : ",plain_txt)
    sleep(wait)
    for char in plain_txt:
        if char in all_letters:
            temp = dict1[char]
            cipher_txt.append(temp)
        else:
            temp =char
            cipher_txt.append(temp)

    cipher_txt= "".join(cipher_txt)
    print("Cipher Text : ",cipher_txt)
    return cipher_txt

inf = s.agentForService(Services.NODE_INFO)
printNodeInformation(inf)
temp = input("Send connection request to node Alice?")
msg = makeAuthRequest(inf.location)
s.send(msg.encode(),11)
print('Request sent to Alice!')
sleep(wait)
print('Awaiting Reply ... ')
msg = s.receive()
from_a = bytearray(msg.data).decode()
print('\nReceived Reply from Alice[11] : ',from_a)
