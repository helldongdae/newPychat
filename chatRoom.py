from Tkinter import *
import networkThread
class show:
	def __init__(self, s):
		self.s = s
		root = Tk()
		text = Text(root)
		self.e = Entry(root, width = 70)
		self.e.pack(side = BOTTOM)
		#t = networkThread(s, e)
		#t.start()
		def func(event):
			text.insert(END, self.e.get()+'\n')
			self.e.delete(0, 'end')
			s.sendall(self.e.get())
		self.e.bind('<Return>', func)
		text.pack()
		root.mainloop()
