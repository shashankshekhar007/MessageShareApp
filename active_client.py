class active_client_list(object):
	def __init__(self):
		self.client_list = []

	def add(self, username):
		self.client_list.append(username)

	def remove(self, username):
		if username in client_list:
			self.client_list.remove(username)
