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
		active_client_list.append(curruser.name)
		#curruser.login()
		clientsocket.mysend(login_message)
		getUsage(clientsocket)	
	else:
		clientsocket.mysend(login_message)
		get_option(clientsocket)


def getUsage(clientsocket):
	print("Entering getUsage")
	try:
		clientsocket.mysend('[1]PrivatChat\n[2]FileSharing\n[3]Broadcast\n')
	except Exception as e:
		raise e
	try:
		choice = clientsocket.myreceive()
	except Exception as e:
		raise e
	print(choice)
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



