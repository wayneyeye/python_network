import argparse,socket
from datetime import datetime
MAX_BYTES=65535
def server(port):
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # defines the udp protocol
	# Get my ipaddress
	my_ip=socket.gethostbyname(socket.gethostname())
	sock.bind((my_ip,port))
	print('Listening at {}'.format(sock.getsockname())) # sock name is a tuple of ip address and port
	while True:
		data, address = sock.recvfrom(MAX_BYTES)
		text=data.decode('utf-8')
		print('The client at {} says {!r}'.format(address,text))
		text= 'Your data was {} bytes long'.format(len(data))
		data=text.encode('utf-8')
		sock.sendto(data,address)

def client(dest,port,text=None):
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # defines the udp protocol
	if text is not None:
		text=text
	else:
		text = 'The time is {}'.format(datetime.now())
	data = text.encode('utf-8')
	delay=0.1 # set the initial wait time
	sock.connect((dest,port))
	print('The OS assigned me the address {}'.format(sock.getsockname()))
	while True:
		# sock.sendto(data,('127.0.0.1',port))
		sock.send(data)
		sock.settimeout(delay)
		try:
			data,address=sock.recvfrom(MAX_BYTES)
			text=data.decode('utf-8')
			print('The server {} replied {!r}'.format(address,text))
		except socket.timeout:
			delay*=2
			if (delay>=2.0):
				raise RuntimeError('Timeout > 2, Force exit!')
		else:
			break
	


if __name__ == '__main__':
	choices={'client':client,'server':server}
	parser=argparse.ArgumentParser(description='Send and receive UDP locally')
	parser.add_argument('role',choices=choices,help='which role to play')
	parser.add_argument('-d',metavar='IP',type=str,default=None,help='Target IP address')
	parser.add_argument('-p',metavar='PORT',type=int,default=1060,help='UDP port to listen (default 1060)')
	parser.add_argument('-m',metavar='MESSAGE',type=str,default=None,help='Customized text message to send')
	args=parser.parse_args()
	function=choices[args.role]
	if args.m is not None:
		client(args.d,args.p,args.m)
	else:
	  function(args.p)
