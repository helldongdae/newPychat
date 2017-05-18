from Tkinter import *
import tkMessageBox
import socket
class show():
	def __init__(self, s):
		self.s = s
		root = Tk()
		e = Entry(root)
		e.pack()
		e.delete(0, END)
		e.insert(0, "USERNAME")
		def func(event):
			s.sendall("USERNAME "+e.get())
			res = s.recv(1024)
    			if res == 'SUCCESS':
				root.destroy()
			else:
				tkMessageBox.showwarning(
            			"Error",
            			"Name already exist"
        			)
		e.bind('<Return>', func)
		root.mainloop()
		
