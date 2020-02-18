output_characters= 'We copy you down, Eagle\n'
output_bytes=output_characters.encode('utf-8')
print(output_bytes)
print(output_bytes.decode())

input_bytes=b'\xff\xfe4\x001\x003\x00'
input_characters=input_bytes.decode('utf-16')
print(input_bytes)
print(repr(input_characters))

print('123\\')
b=bytes([0,1,98,101])
print(b)

# print ascii
for i in range(32,128,32):
	print(' '.join(chr(j) for j in range(i,i+32)))



