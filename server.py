#!/usr/bin/env python3

import socket
import os
import sys
import auth
from serversocketdefinition import mysocket
import time
#import user
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

'''def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." %client_address)
		Thread(target=handle_client, args=(client,)).start()
'''

def get_option(clientsocket):
	try:
		clientsocket.mysend('[1] Signup \n[2] SignIn\n[3] Quit\n')
	except Exception as e:
		raise e
	try:
		option = clientsocket.myreceive()
	except Exception as e:
		raise e
	return option

def sign_up(clientsocket):
	try:
		clientsocket.mysend('Enter Username:Password:Password\n')
	except Exception as e:
		raise e
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
	if 'Successful' in sign:
		return True
	else:
		return False

def sign_in(clientsocket):
	#curruser = user.user(clientsocket)
	try:
		clientsocket.mysend('Enter Username:Password\n')
	except Exception as e:
		raise e
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
		clientsocket.mysend(login_message)
		return True
	else:
		clientsocket.mysend(login_message)
		return False
		#return False
	#curruser.update_cred(l[0],l[1])
	#login_message = curruser.login()
	#clientsocket.mysend(login_message)
	#if 'Successful' in login_message:
	#	return curruser
	#else:
	#	return False


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

SERVER.listen(5)
print("Socket is listening\n")

while True:
	clientsocket, addr = SERVER.accept()
	print("Got connection from", addr)
	newpid = os.fork()
	if newpid<0:
		print("Error in forking")
		sys.exit()
	elif newpid==0:
		flag = 1
		while True:
			option = get_option(clientsocket)

			if option=='1':
				sign_up(clientsocket)
			if option=='2':
				if sign_in(clientsocket):				
					while True:
						usage = getUsage(clientsocket)

				#if curruser:
				#	break
				#else:
				#	continue
		#del(curruser)

		clientsocket.close()
		break
	else:
		clientsocket.close()


