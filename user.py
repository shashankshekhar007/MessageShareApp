import auth
import os

class user:
	def __init__(self, sock, name=None, passwd=None):
		self.name = name
		self.pwd = passwd
		self.path = ""
		self.logged_in = False
		self.sock = sock
	
	def update_cred(self, name, passwd):
		self.name = name
		self.pwd = passwd

	def login(self):
		if "Invalid" in auth.login(self.name, self.pwd):
			del self
			return "Invalid Credentials\n"
		else:
			logged_in = True
			self.path = self.name + '/'
			return "Login Successful\n"
	
	def ls(self):
		files = filter(lambda f: not f.startswith('.'), os.listdir(self.path))
		flist = "\n".join(files)
		return flist

	def i_shared(self):
		f = open(self.path + ".shared", "r")
		slist = f.read()
		f.close()
		return slist

	def shareit(self, filename, who):
		if os.path.isfile(self.path + filename):
			f = open('passwords.txt', 'r')
			entry = f.readline()
			found = False
			while entry != "":
				userpass = entry.split()
				if userpass[0] == who:
					found = True
					break
				entry = f.readline()
			f.close()
			if not found:
				return "User doesn't exist\n"
			f = open(self.path + ".shared", "a+")
			f.write(filename + " " + who +"\n")
			f.close()
			f = open(self.path + "../" + who + "/.shared_with_me", "a+")
			f.write(filename + " " + self.name + "\n")
			f.close()
			return "File shared\n"
		else:
			return "File doesn't exist\n"

	def shared_to_me(self):
		f = open(self.path + ".shared_with_me", "r")
		slist = f.read()
		f.close()
		return slist

	def __exit__(self, *err):
		self.close()
