#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import getpass
import socket
import sys
import auth
from clientsocketdefinition import mysocket

s = mysocket()
port = 12345
ip_address = input("Type the id address to connect to\n")
s.connect(ip_address, port)

while True:
	option = 0
	option_msg = s.myreceive()
	while option not in ['1','2','3']:
		option = input(option_msg)
		if option not in ['1','2','3']:
			print("Error: Enter 1 or 2 or 3")
	s.mysend(option)
	if option=='1':
		username = input("Username:")
		password = getpass.getpass("Password:")
		password_repeat = getpass.getpass("Re-enter Password:")
		s.mysend(username+':'+password+':'+password_repeat)
	if option=='2':
		username = input("Username:")
		password = getpass.getpass("Password:")
		s.mysend(username+':'+password)
	if option=='3':
		s.close()
		sys.exit()
	login_msg = s.myreceive()
	print(login_msg)
	if 'Successful' in login_msg and option=='2':
		break

while True:
	print("[1]PrivatChat\n[2]FileSharing\n[3]Broadcast\n")
	option = input("Option:")
	while option not in ['1','2','3']:
		option = input(option_msg)
		if option not in ['1','2','3']:
			print("Enter either 1 or 2 or 3")
	s.mysend(option)
	if option=='1':
		privateChat()
	if option=='2':
		fileTransfer()
	if option=='3':
		broadCast()
s.close()
