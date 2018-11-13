import os
import sys
import socket
from socket import AF_INET, SOCK_STREAM

class mysocket(object):
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		else:
			self.sock = sock

	def bind(self, ipaddress, port):
		self.sock.bind((ipaddress , port))

	def connect(self, host, port):
		self.sock.connect((host, port))
	
	def listen(self, num_clients):
		self.sock.listen(num_clients)

	def accept(self):
		c, addr = self.sock.accept()
		clientSocket = mysocket(c)
		return [clientSocket, addr]
	
	def close(self):
		self.sock.close()

	def mysend(self, msg):
		MSGLEN = len(msg)
		length = str(MSGLEN)
		if len(length) <= 10:
			length = '0'*(10-len(length))+ length
		else:
			print("Increased length")
		msg = length+msg
		totalsent = 0
		while totalsent < MSGLEN+10:
			sent = self.sock.send((msg[totalsent:]).encode('utf-8'))
			if sent==0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def myreceive(self):
		MSGLEN = int((self.sock.recv(10)).decode('utf-8'))
		chunks = []
		bytes_recd = 0
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048)).decode('utf-8')
			if chunk=='':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return ''.join(chunks)
