from Tkinter import *
import tkMessageBox
class show:
	def __init__(self, s):
		self.s = s
		self.t = False
		root = Tk()
		listbox = Listbox(root, selectmode=MULTIPLE)
		listbox.pack()
		def refreshCallback():
			s.sendall('REFRESH')
			res = s.recv(1024)
			res = res.split()
			listbox.delete(0, END)
			for i in res:
				listbox.insert(END, i)

		def doneCallback():
			selection = listbox.curselection()
			props = ''
			for i in selection:
				props += listbox.get(i)+' '
			print props
			e = Entry(root)
			e.pack(side = BOTTOM)
			def func(event):
				self.s.sendall("PROP "+str(len(selection))+" "+props+e.get())
			e.bind('<Return>', func)

		b = Button(root, text="refresh", command=refreshCallback)
		b.pack()
		b2 = Button(root, text="done", command=doneCallback)
		b2.pack()
		root.mainloop()

