from Tkinter import *
import threading
import socket

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
		self.e.insert(END, data+'\n')
		return thread(self.s, self.e).start()

    	def stop(self):
		self._stop.set()
