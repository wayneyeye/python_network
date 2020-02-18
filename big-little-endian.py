import struct
print(struct.pack('<i',4253))
print(struct.pack('>i',4253))

# socket
print(struct.pack('!i',4253))
# unpack
print(struct.unpack('!i',(struct.pack('!i',4253))))

