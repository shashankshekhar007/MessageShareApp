#!/usr/bin/env python3

import socket
import os
import sys
import auth
from serversocketdefinition import mysocket
import time
import user
#from active_client import active_client_list
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		clientsocket, address = SERVER.accept()
		print("%s:%s has connected." %address)
		Thread(target=get_option, args=(clientsocket,)).start()


active_client_list= []
socketadd ={}
sockettoname={}

def newChat(clientsocket, tousersocket):
	while True:
		try:
			msg1 = clientsocket.myreceive()
			if msg1=="Quit":
				tousersocket.mysend("Quit")
				break
		except Exception as e:
			raise e
		else:
			msg2 = tousersocket.mysend(sockettoname[tousersocket]+ ">> "+msg1)
	getUsage(clientsocket)

def startp2pChat(p1socket, p2socket):
	Thread1 = Thread(target=newChat, args=(p1socket, p2socket))
	Thread2 = Thread(target=newChat, args=(p2socket, p1socket))
	Thread1.start()
	Thread2.start()


def startChat(clientsocket):
	clientsocket.mysend(str(active_client_list))
	touser = clientsocket.myreceive()
	if touser in active_client_list:
		tousersocket = socketadd[touser]
		clientsocket.mysend("Yes")
		tousersocket.mysend("Someone wants to connect to you")
		yesorno = tousersocket.myreceive()
		print("Reaching here "+ sockettoname[clientsocket])
		if yesorno=='YES':
			startp2pChat(clientsocket, tousersocket)
			
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
	login_message = auth.login(l[0],l[1])
	if 'Successful' in login_message:
		active_client_list.append(l[0])
		socketadd[l[0]] = clientsocket
		sockettoname[clientsocket]= l[0]
		clientsocket.mysend(login_message)
		getUsage(clientsocket)	
	else:
		clientsocket.mysend(login_message)
		get_option(clientsocket)


def sitIdle(clientsocket):
	while True:
		#print(1)
		idlevariable = 1



def getUsage(clientsocket):	
	try:
		choice = clientsocket.myreceive()
	except Exception as e:
		raise e
	if choice=='1':
		startChat(clientsocket)
	if choice=='2':
		fileShare(clientsocket)
	if choice=='3':
		broadCast(clientsocket)
	if choice=='4':
		sitIdle(clientsocket)
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
	# clientsocket, addr = SERVER.accept()
	# print("Got connection from", addr)
	# newpid = os.fork()
	# if newpid<0:
	# 	print("Error in forking")
	# 	sys.exit()
	# elif newpid==0:
	# 	flag = 1
	# 	while True:
	# 		option = get_option(clientsocket)

	# 		if option=='1':
	# 			sign_up(clientsocket)
	# 		if option=='2':
	# 			answer = sign_in(clientsocket)
	# 			if answer:
	# 				print(answer)
	# 				break
	# 				#curruser = answer[0]
	# 				#active_client_list.append(answer[1])
	# 				#print(active_client_list)
	# 				#if curruser:
	# 				#	break
	# 			else:
	# 				continue

	# 	#del(curruser)

	# 	clientsocket.close()
	# 	break
	# else:
	# 	clientsocket.close()
SERVER.close()



