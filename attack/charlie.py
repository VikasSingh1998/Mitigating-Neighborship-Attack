from unetpy import UnetSocket, Services
from routing import printRoutingTable
from datetime import datetime
from time import sleep
import string

s = UnetSocket('localhost',1104)
#inf = s.agentForService(Services.NODE_INFO)
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Timestamp : ",timestamp)

table = [['Alice  ',11,1], ['Bob    ',12, 2],['Charlie',14, 0],['Delta  ',15, 1]]

printRoutingTable(table)

temp = input('Send routing details to Alice?')

msg = 'Bob 12 2'
msg = msg + "|" +timestamp
s.send(msg.encode(),11)
print('Message sent to Alice : ',msg)

print('Awaiting Reply ... ')
msg = s.receive()

s.close()