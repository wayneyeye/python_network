import socket,struct
from argparse import ArgumentParser

# defines a header struct for stipulating the length
header_struct=struct.Struct('!I') # partial function


def recvall(sock,length):
	blocks=[]
	while length:
		block=sock.recv(length)
		if not block:
			raise EOFError('socket closed with %d bytes left in this block' % (length))
		length-=len(block)
		blocks.append(block) # collect all blocks
	return b''.join(blocks)

def get_block(sock):
	data=recvall(sock,header_struct.size)
	(block_length,)=header_struct.unpack(data)
	return recvall(sock,block_length)

def put_block(sock,message):
	block_length=len(message)
	sock.send(header_struct.pack(block_length))
	sock.send(message)

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
	while True:
		message=get_block(sc)
		if not message:
			break
		print(message.decode('ascii'))
	sc.close() # close the connection
	sock.close() # close the listening sock

def client(address):
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # defines the tcp protocol
	sock.connect(address)
	sock.shutdown(socket.SHUT_RD) # only send message	
	put_block(sock,b'Beautiful is better than ugly')
	put_block(sock,b'Beautiful is better than ugly')
	put_block(sock,b'Beautiful is better than ugly')
	put_block(sock,b'') # end of talk, send an empty bytes
	sock.close()


if __name__ == '__main__':
	parser=ArgumentParser(description='Send and receive TCP')
	parser.add_argument('hostname',nargs='?',default='127.0.0.1',help='IP address or hostname (default: %(default)s)')
	parser.add_argument('-c',action='store_true',help='run as the client')
	parser.add_argument('-p',metavar='PORT',type=int,default=1060,help='TCP PORT to listen (default 1060)')
	args=parser.parse_args()
	function = client if args.c else server
	function((args.hostname,args.p))
