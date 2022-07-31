from unetpy import UnetSocket, Services
from myInfo import printNodeInformation
from time import sleep
from datetime import datetime
import string

all_letters = string.digits + string.ascii_letters + string.punctuation
s = UnetSocket('localhost',1101)
wait = 10

def verifyTimestamp(time_sent,time_rec):
    threshold = 5   # threshold set to 5 minutes
    sender_time = datetime.strptime(time_sent,'%Y-%m-%d %H:%M:%S')
    received_time = datetime.strptime(time_rec,'%Y-%m-%d %H:%M:%S')
    print("    Threshold Value (in minutes) : ",threshold)
    print("    Sender's Timestamp : ",sender_time)
    print("    Receiver's Timestamp : ",received_time)
    td_mins = int(round((received_time - sender_time).total_seconds()) / 60)
    print("    Difference (in minutes) : ",td_mins)
    sleep(1)
    if td_mins<=threshold:
        print("    Timestamp Verified!")
        return True
    return False    

def verifyRange(loc_sender,loc_receiver):
    loc_sender = list(map(float,loc_sender.split()))
    print("    Sender Location : ",loc_sender)
    print("    Receiver Location : ",loc_receiver)
    range_info = s.agentsForService(Services.RANGING)
    max_range = range_info[0].maxRange
    actual_range = 0
    for i in range(3):
        actual_range += (loc_receiver[i]-loc_sender[i])**2

    actual_range = actual_range**(1/2)
    print("    Max Range : ",max_range)
    print("    Actual Range : ",actual_range)
    sleep(1)
    if(actual_range <= max_range):
        print("    Range Verified!")
        return True
    return False

def verifyAuthRequest(cipher_txt,timestamp_rec,location_receiver):
    dict2 = {}  
    key = 4   
    for i in range(len(all_letters)):
        dict2[all_letters[i]] = all_letters[(i-key)%(len(all_letters))]
       
    # loop to recover plain text
    decrypt_txt = []
  
    for char in cipher_txt:
        if char in all_letters:
            temp = dict2[char]
            decrypt_txt.append(temp)
        else:
            temp = char
            decrypt_txt.append(temp)
          
    decrypt_txt = "".join(decrypt_txt)
    print("Recovered Plain Text :", decrypt_txt) 
    
    try:
        location, timestamp = decrypt_txt.split('|')
    except:
        return False
    print("Verifying Range...")
    sleep(1)
    if(not verifyRange(location,location_receiver)):
        return False
    print("Verifying Timestamp...")
    sleep(1)
    if(not verifyTimestamp(timestamp,timestamp_rec)):
        return False
    return True

inf = s.agentForService(Services.NODE_INFO)
printNodeInformation(inf)
print('Listening for requests ...')
routes_e = s.receive()
data_e = bytearray(routes_e.data).decode()
timestamp_rec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
sender = routes_e.from_
print('\nConnection request from ['+str(sender)+'] : ',data_e)
temp = input('Start verification?')

if(verifyAuthRequest(data_e,timestamp_rec,inf.location)):
    msg = 'Connection Accepted'
else:
    msg = 'Connection Refused'

print('Message sent to ['+str(sender)+'] : ',msg)
s.send(msg.encode(),sender)

s.close()
