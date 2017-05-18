import threading

class thread(threading.Thread):
 	def __init__(self, sock, e):
        	threading.Thread.__init__(self)
		self._stop = threading.Event()
		self.s = sock
		self.e = e

	def run(self):
		data = self.s.recv(1024)
		if data == 'exit()':
			return
		e.insert(data+'\n')
		return thread(self.s).start()

    	def stop(self):
		self._stop.set()
