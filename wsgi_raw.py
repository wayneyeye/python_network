from pprint import pformat
from wsgiref.simple_server import make_server
import time
def app(environ,start_response):
	host=environ.get('HTTP_HOST','127.0.0.1')
	path=environ.get('PATH_INFO','/')
	query=environ.get('QUERY_STRING','')
	method=environ.get('REQUEST_METHOD','GET')
	if ':' in host:
		host,port=host.split(':',1)
	headers={'Content-Type':'text/plain; charset=utf-8'}
	print(path)
	if method=='GET' and path=='/time':
		start_response('200 OK', list(headers.items()))
		yield time.ctime().encode('ascii')
		yield '\r\n'.encode('utf-8')
		return
	
	#defai;t
	if method=='GET':
		start_response('200 OK', list(headers.items()))
		yield 'OK\r\n'.encode('utf-8')
		yield pformat(environ).encode('utf-8')
		yield '\r\n'.encode('utf-8')
  
if __name__=='__main__':
	httpd=make_server('',8000,app)
	host,port=httpd.socket.getsockname()
	print('Serving on ',host,' port ',port)
	httpd.serve_forever()
	
