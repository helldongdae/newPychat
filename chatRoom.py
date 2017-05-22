from Tkinter import *
import networkThread
import socket
import threading
class show:
	def __init__(self, s, name):
		self.s = s
		self.name = name
		self.s.sendall('IN '+self.name)
		root = Tk()
		text = Text(root)
		listbox = Listbox(root)
		self.e = Entry(root, width = 70)
		self.e.pack(side = BOTTOM)
		self.t = networkThread.thread(self.s, text)
		self.t.start()
		def func(event):
			text.insert(END, self.e.get()+'\n')
			self.s.sendall("CHAT "+self.name+" "+self.e.get())
			self.e.delete(0, 'end')
		self.e.bind('<Return>', func)
		text.pack(side = RIGHT)
		readN = Text(root, width = 5, height = 5)
		readN.pack(side = RIGHT)
		def doubleclickCallback(event):
			self.s.sendall('SEND_ME_EXIT_CODE')
			self.t.join()
			self.s.sendall("ADD_USER"+" "+name+" "+listbox.get(ACTIVE))
			print listbox.get(ACTIVE)
			res = self.s.recv(1024)
			if(res == 'FAIL'):
				text.insert(END, 'He/ She is already in this chatroom'+'\n')
			else:
				text.insert(END, listbox.get(ACTIVE)+' joined'+'\n')
			self.t = networkThread.thread(self.s, text)
			self.t.start()
		listbox.bind('<Double-Button-1>', doubleclickCallback)
		listbox.pack(side = RIGHT)
		def refreshCallback():
			global t
			self.s.sendall('SEND_ME_EXIT_CODE')
			self.t.join()
			self.s.sendall("GET_USER")
			usr = self.s.recv(1024)
			usr = usr.split()
			listbox.delete(0, END)
			for i in usr:
				listbox.insert(END, i)
			self.t = networkThread.thread(self.s, text)
			self.t.start()
				
		b = Button(root, text="refresh", command=refreshCallback)
		b.pack(side = BOTTOM)
		def on_closing():
			self.s.sendall('SEND_ME_EXIT_CODE')
			self.s.sendall('OUT '+self.name)
			root.destroy()
		root.protocol("WM_DELETE_WINDOW", on_closing)
		root.mainloop()
