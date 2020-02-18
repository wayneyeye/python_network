import socket
from time import sleep
from argparse import ArgumentParser

def recvall(sock,length):
	data = b''
	while len(data)<length:
		more = sock.recv(length-len(data))
		if not more:
			raise EOFError('was expecting %d bytes but only %d bytes before the socket closed' % (length,len(data)))
		data+=more
	return data


def server(address):
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # defines the tcp protocal STREAM
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind(address)
	sock.listen(1)
	print("Run this script in another window with -c to connect")
	# this sock will only accept connections but not in charge of transfer data
	print('Listening at {}'.format(sock.getsockname())) # sock name is a tuple of ip address and port
	sc,sockname=sock.accept()
	print('Accepted connection from ',sockname)
	sc.shutdown(socket.SHUT_WR) # close the write from the server side, only listens from the client to avoid DEADLOCK
	message=b''
	while True:
		more = sc.recv(8192)
		if not more:
			print("Received zero bytes -- end")
			break
		print('Received {} bytes'.format(len(more)))
		message+=more
	print('Message:\n')
	print(message.decode('ascii'))
	sc.close() # close the connection
	sock.close() # close the listening sock

def client(address):
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # defines the tcp protocol
	sock.connect(address)
	sock.shutdown(socket.SHUT_RD) # only send message	
	sock.sendall(b'Beautiful is better than ugly\n')
	sleep(1) # this will clear the buffer
	sock.sendall(b'Explicit is better than implicit')
	sock.close()


if __name__ == '__main__':
	parser=ArgumentParser(description='Send and receive TCP')
	parser.add_argument('hostname',nargs='?',default='127.0.0.1',help='IP address or hostname (default: %(default)s)')
	parser.add_argument('-c',action='store_true',help='run as the client')
	parser.add_argument('-p',metavar='PORT',type=int,default=1060,help='TCP PORT to listen (default 1060)')
	args=parser.parse_args()
	function = client if args.c else server
	function((args.hostname,args.p))
