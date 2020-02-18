import argparse,socket
from datetime import datetime

def recvall(sock,length):
	data = b''
	while len(data)<length:
		more = sock.recv(length-len(data))
		if not more:
			raise EOFError('was expecting %d bytes but only %d bytes before the socket closed' % (length,len(data)))
		data+=more
	return data


def server(interface,port):
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # defines the tcp protocal STREAM
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind((interface,port))
	sock.listen(1) # setup listening at the socket definition 1 is the level of backlog(queue)
	# this sock will only accept connections but not in charge of transfer data
	print('Listening at {}'.format(sock.getsockname())) # sock name is a tuple of ip address and port
	while True:
		sc,sockname=sock.accept() # accept and create a new socket for data transfer (tuple4)
		print('We have accepted a connection from ',sockname)
		print('	SockName ',sc.getsockname())
		print(' SocketPeer',sc.getpeername())
		message = recvall(sc,16)
		print(' Incoming Hex Message:',repr(message))
		sc.sendall(b'Farewell, client')
		sc.close()
		print('	Reply sent socket closed')

def client(host,port):
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # defines the tcp protocol
	sock.connect((host,port))
	print ('Client has been assigned socket name',sock.getsockname())
	sock.sendall(b'Hi there, server! This is a very very long message')
	#sock.sendall(b'Hi !')
	#sock.close()
	sock.shutdown(socket.SHUT_WR)	
	reply=recvall(sock,4)
	print ('Serve said: ',repr(reply))


if __name__ == '__main__':
	choices={'client':client,'server':server}
	parser=argparse.ArgumentParser(description='Send and receive TCP')
	parser.add_argument('role',choices=choices,help='which role to play')
	parser.add_argument('-H',metavar='HOST',type=str,default='127.0.0.1',help='HOST to connect (default 127.0.0.1)')
	parser.add_argument('-p',metavar='PORT',type=int,default=1060,help='TCP PORT to listen (default 1060)')
	args=parser.parse_args()
	function=choices[args.role]
	function(args.H,args.p)
