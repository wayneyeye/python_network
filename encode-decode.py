output_characters= 'We copy you down, Eagle\n'
output_bytes=output_characters.encode('utf-8')
print(output_bytes)
print(output_bytes.decode())

input_bytes=b'\xff\xfe4\x001\x003\x00'
input_characters=input_bytes.decode('utf-16')
print(input_bytes)
print(repr(input_characters))
