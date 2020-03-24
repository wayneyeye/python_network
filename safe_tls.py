# Simple TLS client and server
import argparse,socket,ssl
def client(host,port,cafile=None):
	# use SERVER AUTH on client side
	purpose=ssl.Purpose.SERVER_AUTH
	print(cafile)
	context=ssl.create_default_context(purpose,cafile=cafile)
	# get a raw tcp socket
	raw_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	raw_sock.connect((host,port))
	print('Connected to host {!r} and port {}'.format(host,port))

	# wrap by a ssl context
	ssl_sock=context.wrap_socket(raw_sock,server_hostname=host)
	
	# use as if a normal socket
	while True:
		data=ssl_sock.recv(1024)
		if not data:
			break
		print(repr(data))


def server(host,port,certfile,cafile=None):
	# use CLIENT AUTH on server side
	purpose=ssl.Purpose.CLIENT_AUTH
	context=ssl.create_default_context(purpose,cafile=cafile)
	context.load_cert_chain(certfile) # the server cert (secret)

	# get a raw tcp socket thru the nominal socket
	listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	listener.bind((host,port))
	listener.listen(1)
	print('Listening at interface {!r} and port {}'.format(host,port))
	raw_sock,address=listener.accept()
	print('Connection established from {!r} and port {}'.format(*address))
	# wrap by a ssl context
	ssl_sock=context.wrap_socket(raw_sock,server_side=True)

	# use as if a normal server side socket
	ssl_sock.sendall('Simple is better than complex'.encode('ascii'))
	ssl_sock.close()


if __name__ == '__main__':
	parser=argparse.ArgumentParser(description='Safe TLS client and server')
	parser.add_argument('host',help='hostname or IP address')
	parser.add_argument('port',type=int,help='TCP port number')
	parser.add_argument('-a',metavar='cafile',default=None,help='auth: path to CA pem file')
	parser.add_argument('-s',metavar='certfile',default=None,help='auth: path to server pem file')
	args=parser.parse_args()
	if args.s:
		server(args.host,args.port,args.s,args.a)
	else:
		client(args.host,args.port,args.a)
