#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import getpass
import socket
import sys
import auth
import term
import time
from clientsocketdefinition import mysocket
import os

sock = mysocket()
port = 12345 
ip_address = input("Type the ip address to connect to\n")
sock.connect(ip_address, port)


def receive():
	while True:
		msg= sock.myreceive()
		if (msg=="Someone wants to connect to you"):
			sock.mysend("YES")
			print("New chat started")
		if msg=="Quit":
			print("Quit received")
			break
		else:
			print(msg)
        


def sitIdle():
	while True:
		try:
			msg = sock.myreceive()
			if msg=="Someone wants to connect to you":
				sock.mysend("YES")
				startChat()
				break
		except Exception as e:
			continue
		else:
			print(msg)
			continue
	return


def startChat():
	receive_thread = Thread(target= receive)
	receive_thread.start()
	while True:
		msg1 = input("")
		if msg1=="Quit":
			sock.mysend(msg1)
			return
		sock.mysend(msg1)
	return
	


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
			if msg1=="Quit":
				sock.mysend(msg1)
				break
			sock.mysend(msg1)
		return
	

def broadCast():
	receive_thread = Thread(target = receive)
	receive_thread.start()
	while True:
		msg1 = input(">>")
		if msg1=="Quit":
			sock.mysend(msg1)
			time.sleep(2)
			return 
		sock.mysend(msg1)



def fileTransfer():
	while True:
		options = 'Enter \n[1] List Files\n[2] Upload File\n[3] Download File \n[4] Delete File\n[5] Give Access\n[6] Revoke Access\n[7] Shared Files\n[8] Exit\n'
		print(options)
		choice = input("Your Choice")
		while choice not in ['1','2','3','4','5','6','7','8']:
			print("Error, Enter valid option")
			choice = input("Your Choice")
			if choice not in ['1','2','3','4','5','6','7','8']:
				print(options)
				print("Error, Enter valid option")
		sock.mysend(choice)
		if choice=='1':
			msg1= sock.myreceive()
			print(msg1)

		if choice == '2':
			filename = input("Enter filename:- ")
			if os.path.isfile(filename):
				f = open(filename, "r")
				filedata = f.read()
				f.close()
				sock.mysend(os.path.basename(filename))
				print(sock.myreceive())
				sock.mysend(filedata)
			else:
				sock.mysend("#####----#####")
				print("File doesn't exist!!\n")

		elif choice == '3':
			filename = input("Enter file name: ")
			filename = os.path.basename(filename)
			sock.mysend(filename)
			filedata = sock.myreceive()
			#print(filedata)
			if "File doesn't exist!!\n" == filedata:
				print (filedata)
			else:
				with open(filename, 'w') as outfile:
					outfile.write(filedata)
				print("File Transferred!!")

		elif choice == '4':
			filename = input("Enter file name: ")
			filename = os.path.basename(filename)
			sock.mysend(filename)
			print(sock.myreceive())

		elif choice in ['5','6']:
			filename= input("Enter file name: ")
			username= input("Enter username: ")
			l = filename + ":" + username
			try:				
				sock.mysend(l)
			except Exception as e:
				raise e
			try:
				print(sock.myreceive())
			except Exception as e:
				raise e
		elif choice =='7':
			print(sock.myreceive())
		elif choice == '8':
			return
		

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
		print("[1]PrivatChat\n[2]FileSharing\n[3]Broadcast\n[4]Idle\n[5]Logout")
		option = input("Option:")
		while option not in ['1','2','3','4','5']:
			option = input(option_msg)
			if option not in ['1','2','3','4','5']:
				print("Enter either 1 or 2 or 3 or 4 or 5")
		sock.mysend(option)
		if option=='1':
			privateChat()
		if option=='2':
			fileTransfer()
		if option=='3':
			broadCast()
		if option=='4':
			sitIdle()
		if option=='5':
			break
	sock.close()

renew()
