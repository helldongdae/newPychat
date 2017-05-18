import insertName
import socket
import choose_chatRoom

try: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 8080))
except:
	print 'Can not connect to server'
	exit()

insertName.show(s)

choose_chatRoom.show(s)


