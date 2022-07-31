from unetpy import UnetSocket, Services
from routing import printRoutingTable
from datetime import datetime
from time import sleep
import string

table = [['Alice  ',11,1], ['Bob    ',12, -1],['Evil   ',13,0],['Charlie',14, 1],['Delta  ',15, 1]]

printRoutingTable(table)

s = UnetSocket('localhost',1103)
#inf = s.agentForService(Services.NODE_INFO)
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Timestamp : ",timestamp)
temp = input('Send routing details to Alice?')

msg = 'Bob 12 1'
msg = msg + "|" + timestamp
s.send(msg.encode(),11)
print('Message sent to Alice : ',msg)

print('Listening to Alice\'s Reply ... ')
msg = s.receive()
from_a = bytearray(msg.data).decode()
print('\nReceived Reply from Alice[11] : ')
print(from_a)
print('Neighborship Attack Successful')

s.close()