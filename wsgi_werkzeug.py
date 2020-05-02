import time
from wsgiref.simple_server import make_server
from werkzeug.wrappers import Request, Response
@Request.application
def app(request):
	host=request.host
	if ':' in host:
		host,port=host.split(':',1)
	if request.method != 'GET':
		return Response('501 not implemented',status=501)
	elif host != '127.0.0.1' or request.path!='/time':
		return Response('404 not found',status=404)
	else:
		return Response(time.ctime())
if __name__=='__main__':
        httpd=make_server('',8000,app)
        host,port=httpd.socket.getsockname()
        print('Serving on ',host,' port ',port)
        httpd.serve_forever()	
