from unetpy import UnetSocket, Services
from datetime import datetime
from time import sleep

s = UnetSocket('localhost',1103)

msg = 'Bob 12 1'
s.send(msg.encode(),11)
print('Message sent to Alice : ',msg)

print('Listening to Alice\'s Reply ... ')
msg = s.receive()
from_a = bytearray(msg.data).decode()
print('\nReceived Reply from Alice[11] : ',from_a)

msg = s.receive()
s.close()