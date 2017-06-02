from Tkinter import *
import threading
import socket

class thread(threading.Thread):
 	def __init__(self, sock, e, p):
        	threading.Thread.__init__(self)
		self._stop = threading.Event()
		self.s = sock
		self.e = e
		self.p = p

	def run(self):
		data = self.s.recv(1024)
		if data == 'exit()':
			return
		if data.find('PROP') == 0:
			self.p.delete(1.0, END)
			self.p.insert(END, data[5])
			self.e.insert(END, data[6:len(data)+1]+'\n')
		else:
			self.e.insert(END, data+'\n')
		return thread(self.s, self.e, self.p).start()

    	def stop(self):
		self._stop.set()
