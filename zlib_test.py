import zlib
from time import sleep
message=("我的名字叫韦恩")
data=zlib.compress("准备传送数据".encode('utf-8'))+(b'x'+zlib.compress(message.encode('utf-8')))*3
#print(data)
# initialize a decompressor
d=zlib.decompressobj()
result=b''
loc=0
while loc<len(data):
	result=result+d.decompress(data[loc:loc+8])
	loc=loc+8
	if d.unused_data == b'':
		pass
	else:
		print(result.decode('utf-8'))
		print("--------------------------------")
		loc=loc-len(d.unused_data)+1
		d=zlib.decompressobj()
		result=b''
print(result.decode('utf-8'))
