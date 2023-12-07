import time

class Hub:
	def __init__(self, main_thread_channel, root_directory):
		self.clients = {}
		self.broadcast = []
		self.register = []
		self.unregister = []
		self.main_thread_channel = main_thread_channel
		self.inactive_time = 0
		self.root_directory = root_directory

	def run(self):
		ticker = time.time()

		while True:
			if self.register:
				client = self.register.pop(0)
				print("WS Client registered")
				self.clients[client] = True

			if self.unregister:
				client = self.unregister.pop(0)
				print("WS Client unregistered")
				if client in self.clients:
					del self.clients[client]
					client.send.close()

			if self.broadcast:
				message = self.broadcast.pop(0)
				for client in self.clients:
					try:
						client.send(message)
					except:
						client.send.close()
						del self.clients[client]

			if time.time() - ticker >= 1:
				self.inactive_time += 1
				ticker = time.time()