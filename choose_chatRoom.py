from Tkinter import *
import tkMessageBox
import chatRoom
import propagate
class show:
	def __init__(self, s):
		self.s = s
		self.t = False
		root = Tk()
		listbox = Listbox(root)
		listbox.pack()
		def refreshCallback():
			s.sendall('REFRESH')
			res = s.recv(1024)
			res = res.split()
			listbox.delete(0, END)
			for i in res:
				listbox.insert(END, i)

		def newCallback():
			if self.t == True:
				return
			else:
				self.t = True
			e = Entry(root)
			e.pack(side = BOTTOM)
			def func(event):
				s.sendall("NEW_ROOM "+e.get())
				res = s.recv(1024)
				if res == 'SUCCESS':
					tkMessageBox.showwarning(
            					"Alert",
            					"Success please refresh"
        				)
				else:
					tkMessageBox.showwarning(
            					"Error",
            					"Name already exist"
        				)
				t = False
			e.bind('<Return>', func)

		def doubleclickCallback(event):
			chatRoom.show(self.s, listbox.get(ACTIVE))

		def propCallback():
			propagate.show(self.s)

		b = Button(root, text="refresh", command=refreshCallback)
		b.pack()
		b2 = Button(root, text="new", command=newCallback)
		b2.pack()
		b3 = Button(root, text="prop", command=propCallback)
		b3.pack()
		listbox.bind('<Double-Button-1>', doubleclickCallback)
		root.mainloop()

