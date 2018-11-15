#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import getpass
import socket
import sys
import auth
from clientsocketdefinition import mysocket

sock = mysocket()
port = 12345
ip_address = input("Type the id address to connect to\n")
sock.connect(ip_address, port)


def receive():
	print("This")
	while True:
		msg= sock.myreceive()
		if (msg=="Someone wants to connect to you"):
			sock.mysend("YES")
			print("New chat started")
		if msg=="Quit":
			print("Quit received")
			sock.mysend("Quit")
			#renew()
		if msg=="Renew":
			renew()
		else:
			print(msg)
        


def sitIdle():
	while True:
		try:
			msg = sock.myreceive()
			if msg=="Someone wants to connect to you":
				sock.mysend("YES")
				startChat()
		except Exception as e:
			continue
		else:
			continue


def startChat():
	receive_thread = Thread(target= receive)
	receive_thread.start()
	while True:
		msg1 = input("")
		sock.mysend(msg1)
	


def privateChat():
	userlist = sock.myreceive()
	print(userlist)
	touser = input("\nEnter the user with whom you want to talk\n")
	sock.mysend(touser)
	ans= sock.myreceive()
	if ans=='Yes':
		print("Connection Accepted")
		receive_thread = Thread(target= receive)
		receive_thread.start()
		while True:
			msg1 = input("")
			sock.mysend(msg1)	
	


while True:
	option = 0
	option_msg = sock.myreceive()
	while option not in ['1','2','3']:
		option = input(option_msg)
		if option not in ['1','2','3']:
			print("Error: Enter 1 or 2 or 3")
	sock.mysend(option)
	if option=='1':
		username = input("Username:")
		password = getpass.getpass("Password:")
		password_repeat = getpass.getpass("Re-enter Password:")
		sock.mysend(username+':'+password+':'+password_repeat)
	if option=='2':
		username = input("Username:")
		password = getpass.getpass("Password:")
		sock.mysend(username+':'+password)
	if option=='3':
		sock.close()
		sys.exit()
	login_msg = sock.myreceive()
	print(login_msg)
	if 'Successful' in login_msg and option=='2':
		break


def renew():
	while True:
		print("[1]PrivatChat\n[2]FileSharing\n[3]Broadcast\n[4]Idle")
		option = input("Option:")
		while option not in ['1','2','3','4']:
			option = input(option_msg)
			if option not in ['1','2','3','4']:
				print("Enter either 1 or 2 or 3 or 4")
		sock.mysend(option)
		if option=='1':
			privateChat()
		if option=='2':
			fileTransfer()
		if option=='3':
			broadCast()
		if option=='4':
			sitIdle()
	sock.close()

while True:
	print("[1]PrivatChat\n[2]FileSharing\n[3]Broadcast\n[4]Idle")
	option = input("Option:")
	while option not in ['1','2','3','4']:
		option = input(option_msg)
		if option not in ['1','2','3','4']:
			print("Enter either 1 or 2 or 3 or 4")
	sock.mysend(option)	
	if option=='1':		
		privateChat()
	if option=='2':
		fileTransfer()
	if option=='3':
		broadCast()
	if option=='4':
		sitIdle()
sock.close()