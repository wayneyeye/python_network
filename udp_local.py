import argparse,socket
from datetime import datetime
MAX_BYTES=65535
def server(port):
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # defines the udp protocol
	sock.bind(('127.0.0.1',port))
	print('Listening at {}'.format(sock.getsockname())) # sock name is a tuple of ip address and port
	while True:
		data, address = sock.recvfrom(MAX_BYTES)
		text=data.decode('utf-8')
		print('The client at {} says {!r}'.format(address,text))
		text= 'Your data was {} bytes long'.format(len(data))
		data=text.encode('utf-8')
		sock.sendto(data,address)

def client(port):
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # defines the udp protocol
	text = 'The time is {}'.format(datetime.now())
	data = text.encode('utf-8')
	sock.sendto(data,('127.0.0.1',port))
	print('The OS assigned me the address {}'.format(sock.getsockname()))
	data,address=sock.recvfrom(MAX_BYTES)
	text=data.decode('utf-8')
	print('The server {} replied {!r}'.format(address,text))
	



if __name__ == '__main__':
	choices={'client':client,'server':server}
	parser=argparse.ArgumentParser(description='Send and receive UDP locally')
	parser.add_argument('role',choices=choices,help='which role to play')
	parser.add_argument('-p',metavar='PORT',type=int,default=1060,help='UDP port to listen (default 1060)')
	args=parser.parse_args()
	function=choices[args.role]
	function(args.p)
