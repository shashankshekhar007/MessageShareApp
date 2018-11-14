import os
import hashlib

activeusers=[]
def signup(user, passwd, pass_repeat):
	if passwd != pass_repeat:
		return "Passwords do not match\n"
	elif ' ' in user or ' ' in passwd:
		return "Cannot contain spaces\n"
	else:
		f = open('passwords.txt', 'r+', encoding='utf-8')
		entry = f.readline()
		while entry!= "":
			userpass = entry.split()
			if userpass[0] == user:
				return "Username alredy exists\n"
			entry = f.readline()

		f.write(user + " " + (hashlib.md5(passwd.encode('utf-8')).hexdigest()) + "\n")
		f.close()
		os.makedirs(user)
		f = open(user + '/.shared','w+')
		f.close()
		f = open(user + '/.shared_with_me', 'w+')
		f.close()
		return "Successful signup\n"

def login(user, passwd):
	passwd1 = hashlib.md5(passwd.encode('utf-8')).hexdigest()
	f = open('passwords.txt')
	entry = f.readline().strip('\n')
	# print("Entry is %s\n" %entry)
	while entry != "":
		userpass = entry.split(' ')
		if userpass[0] == user and userpass[1] == passwd1:
			activeusers.append(user)
			return "Login Successful\n"
		entry = f.readline().strip('\n')
	
	f.close()
	return "Invalid credentials"
