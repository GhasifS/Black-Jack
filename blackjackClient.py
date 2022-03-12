# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:18:17 2021

@author: Ghasif, Yehua, Tong
"""

# Imports
import socket

# Establish connection with server
ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 1233
ClientSocket.connect(('127.0.0.1', port))

# Receive initial response from server
response = ClientSocket.recv(1024)
print(response.decode('utf-8'))

# While loop that maintains communication between the client and server back and forth
while True:
    userInput = input('Give your input: ')
    ClientSocket.send(str.encode(userInput))
    response = ClientSocket.recv(1024)
    print(response.decode('utf-8'))
ClientSocket.close()