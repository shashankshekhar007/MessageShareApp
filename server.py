#!/usr/bin/env python3

import socket
import os
import sys
import auth
from serversocketdefinition import mysocket
import time
import user
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		clientsocket, address = SERVER.accept()
		print("%s:%s has connected." %address)
		Thread(target=get_option, args=(clientsocket,)).start()


active_client_list= {}
socketadd ={}
sockettoname={}



def get_next_action(clientsocket,curruser):
	while True:
		try:
			option = clientsocket.myreceive()
		except Exception as e:
			raise e
		if option == '0':
			try:
				clientsocket.mysend('Enter \n[0] HELP \n[1] List Files\n[2] Upload File\n[3] Download File \n[4] Delete File\n[5] Give Access\n[6] Revoke Access\n[7] Shared Files\n[8] Exit\n')
			except Exception as e:
				raise e
		if option == '1':
			try:
				clientsocket.mysend(curruser.ls()+'\nShared Files: \n'+curruser.shared_to_me())
			except Exception as e:
				raise e

		if option == '2':      
			try:
				filename = clientsocket.myreceive()
			except Exception as e:
				raise e
			if filename =='#####----#####':
				continue
			try:
				clientsocket.mysend("Transferring File............\n")
			except Exception as e:
				raise e
			try:
				filedata = clientsocket.myreceive()
			except Exception as e:
				raise e
			curruser.writefile(filename, filedata)

		if option == '3':      
			try:
				filename = clientsocket.myreceive()
			except Exception as e:
				raise e
			print("Going to see the file now")
			filedata = curruser.readfile(filename)
			print("Seen the file")
			print(filedata)
			if "File doesn't exist!!\n" == filedata:
				filedata = curruser.shared_read(filename)
				if "File is not shared with you!!\n" == filedata:
					try:
						clientsocket.mysend("File doesn't exist!!\n")
					except Exception as e:
						raise e
				else:
					try:
						clientsocket.mysend(filedata)
					except Exception as e:
						raise e
			else:
				try:
					clientsocket.mysend(filedata)
				except Exception as e:
					raise e
		if option == '4':
			try:
				filename = clientsocket.myreceive()
			except Exception as e:
				raise e
			delete_msg = curruser.deletefile(filename)
			try:
				clientsocket.mysend(delete_msg)
			except Exception as e:
				raise e
		if option == '5':
			try:
				l = clientsocket.myreceive().strip('\n').split(':')
			except Exception as e:
				raise e
			msg = curruser.shareit(l[0],l[1])
			try:
				clientsocket.mysend(msg)
			except Exception as e:
				raise e

		if option == '6':			
			try:
				l = clientsocket.myreceive().strip('\n').split(':')
			except Exception as e:
				raise e
			msg = curruser.takeback(l[0],l[1])
			try:
				clientsocket.mysend(msg)
			except Exception as e:
				raise e

		if option == '7':
			try:
				clientsocket.mysend(curruser.i_shared())
			except Exception as e:
				raise e

		if option == '8':
			try:
				clientsocket.mysend("Closing Connection...\n")
			except Exception as e:
				raise e
			return



def newChat(clientsocket, tousersocket,curruser):
	while True:
		try:
			msg1 = clientsocket.myreceive()
			if msg1=="Quit":
				tousersocket.mysend("Quit")
				break
		except Exception as e:
			raise e
		else:

			msg2 = tousersocket.mysend(sockettoname[clientsocket]+ ">> "+msg1)
	getUsage(clientsocket)

def startp2pChat(p1socket, p2socket,curruser):
	print("Starting chat between "+sockettoname[p1socket]+" and "+ sockettoname[p2socket])
	Thread1 = Thread(target=newChat, args=(p1socket, p2socket,curruser))
	Thread2 = Thread(target=newChat, args=(p2socket, p1socket,curruser))
	Thread1.start()
	Thread2.start()


def startChat(clientsocket,curruser):
	clientsocket.mysend(str(active_client_list))
	touser = clientsocket.myreceive()
	if touser in active_client_list:
		tousersocket = socketadd[touser]
		clientsocket.mysend("Yes")
		tousersocket.mysend("Someone wants to connect to you")
		yesorno = tousersocket.myreceive()
		print("Reaching here "+ sockettoname[clientsocket])
		if yesorno=='YES':
			startp2pChat(clientsocket, tousersocket,curruser)
			
def get_option(clientsocket):
	try:
		clientsocket.mysend('[1] Signup \n[2] SignIn\n[3] Quit\n')
	except Exception as e:
		raise e
	try:
		option = clientsocket.myreceive()
	except Exception as e:
		raise e
	if option=='1':
		sign_up(clientsocket)
	if option=='2':
		sign_in(clientsocket)
	if option=='3':
		clientsocket.close()
		return 

def sign_up(clientsocket):	
	try:
		creds = clientsocket.myreceive()
	except Exception as e:
		raise e
	if creds.count(':')!=2:
		clientsocket.mysend('Not appropriate information\n')
		return False

	l = creds.strip('\n').split(':')
	sign = auth.signup(l[0],l[1],l[2])
	try:
		clientsocket.mysend(sign)
	except Exception as e:
		raise e
	get_option(clientsocket)


def sign_in(clientsocket):
	curruser = user.user(clientsocket)	
	try:
		creds = clientsocket.myreceive()
	except Exception as e:
		raise e
	
	if creds.count(':') != 1:
		clientsocket.mysend('Information not appropriate\n')
		return False

	l = creds.strip('\n').split(':')
	curruser.update_cred(l[0],l[1])
	login_message= curruser.login()
	#login_message = auth.login(l[0],l[1])
	if 'Successful' in login_message:
		active_client_list[l[0]]='0'
		socketadd[l[0]] = clientsocket
		sockettoname[clientsocket]= l[0]
		clientsocket.mysend(login_message)
		getUsage(clientsocket,curruser)	
	else:
		clientsocket.mysend(login_message)
		get_option(clientsocket)


def sitIdle(clientsocket):
	while True:
		#print(1)
		idlevariable = 1


def broadCast(clientsocket,curruser):
	while True:
		try: 
			msg= clientsocket.myreceive()
			if (msg=="Quit"):
				for member in active_client_list:
					if active_client_list[member] in ['3','4']:
						socketadd[member].mysend(sockettoname[clientsocket] + " has left the chat")
				clientsocket.mysend("Quit")
				active_client_list[sockettoname[clientsocket]]='0'
				getUsage(clientsocket,curuser)
				return
		except Exception as e:
			raise e
		else:
			for member in active_client_list:
				if active_client_list[member] in ['3','4']:
					socketadd[member].mysend(sockettoname[clientsocket] +": "+  msg);

def getUsage(clientsocket,curruser=None):	
	try:
		choice = clientsocket.myreceive()
	except Exception as e:
		raise e
	if choice=='1':
		active_client_list[sockettoname[clientsocket]]='1'
		startChat(clientsocket,curruser)
	if choice=='2':
		active_client_list[sockettoname[clientsocket]]='2'
		get_next_action(clientsocket,curruser)
		getUsage(clientsocket,curruser)
	if choice=='3':
		active_client_list[sockettoname[clientsocket]]='3'
		broadCast(clientsocket,curruser)
		#getUsage(clientsocket)
	if choice=='4':
		active_client_list[sockettoname[clientsocket]]='4'
		sitIdle(clientsocket)
	if choice=='5':
		del active_client_list[sockettoname[clientsocket]]
		clientsocket.close()
	return


port = 12345
if len(sys.argv)!=2:
	print("Insufficient arguments")
SERVER = mysocket()
host = sys.argv[1]
print("Socket successfully created\n")

SERVER.bind(host, port)
print("Socket bound to %s" %port)

SERVER.listen(10)
print("Socket is listening\n")

while True:
	ACCEPT_THREAD = Thread(target = accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	
SERVER.close()



