# simulate {
#   node 'Alice', address:11, location: [ 0.km, 0.km, -15.m], web: 8081, api: 1101, stack: "$home/etc/setup"
#   node 'Bob', address:12, location: [ 4.km, 0.km, -15.m], web: 8082, api: 1102, stack: "$home/etc/setup"
#   node 'Evil', address:13, location: [ 200.m, 0.km, -15.m], web: 8083, api: 1103, stack: "$home/etc/setup"
#   node 'Charlie', address:14, location: [ 800.m, 500.m, -15.m], web: 8084, api: 1104, stack: "$home/etc/setup"
#   node 'Delta', address:15, location: [ 2500.km, 500.m, -15.m], web: 8085, api: 1105, stack: "$home/etc/setup"
# }

'''
************ FLOW *************     
Actual NW of nodes A,B,C,D
Evil enters NW
A wants to send message to B
C sends routes info to A C->D->B
Evil sends routes info to A E->B
A chooses shortest route A->E->B
A sends messages to Evil
Evil's neighborship attack successful
'''


from unetpy import UnetSocket, Services
from routing import printRoutingTable
from time import sleep
from datetime import datetime
import string

s = UnetSocket('localhost',1101)

table = [['Alice  ',11,0], ['Bob    ',12, -1],['Charlie',14, 1],['Delta  ',15, 2]]
time_rec = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #timestamp_receiving
printRoutingTable(table)

#sender_time = datetime.strptime(time_sent,'%Y-%m-%d %H:%M:%S')
timestamp_at_alice = datetime.strptime(time_rec,'%Y-%m-%d %H:%M:%S')


routes_c = s.receive()
data_c = bytearray(routes_c.data).decode()
c_msg, c_time_sent = data_c.split('|')
c_timestamp = datetime.strptime(c_time_sent,'%Y-%m-%d %H:%M:%S')
time_taken_by_charlie = int((timestamp_at_alice - c_timestamp).total_seconds())
print('\nMessage received from Charlie[14] : ',c_msg)
print('\nMessage received from Charlie[14] in time : ',-time_taken_by_charlie,'seconds')


routes_e = s.receive()
data_e = bytearray(routes_e.data).decode()
e_msg, e_time_sent = data_e.split('|')
e_timestamp = datetime.strptime(e_time_sent,'%Y-%m-%d %H:%M:%S')
time_taken_by_evil = int((timestamp_at_alice - e_timestamp).total_seconds())
print('\nMessage received from Evil[13] : ',e_msg)
print('\nMessage received from Evil[13] in time : ',-time_taken_by_evil,'seconds')

sleep(1)
print('Searching address [13] in routing table ...')
sleep(1)
new = ['Evil   ', 13, 1]
print('Address[13] not found\nAdding new entry ',*new)
sleep(1)
print('Selecting shorter route Alice->Evil->Bob\nUpdating distance to Bob : 2 hops')
sleep(1)
print('Creating new routing table...')
sleep(1)

table.append(new)
table[1][2] = 2
printRoutingTable(table)
sleep(1)

print('Sending messages to Bob via Evil...')
sleep(1)

msg = 'Connection Accepted'
print('Message sent to Evil : ',msg)
s.send(msg.encode(),13)

s.send('Connection Refused'.encode(),14)

s.close()
