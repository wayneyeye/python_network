import memcache,random,time,timeit
def compute(mc,n):
	value=mc.get('sq:%d' % n)
	if value is None:
		# similuate a long run computation
		time.sleep(0.001)
		value=n*n
		mc.set('sq:%d' % n,value)
	return value

def main():
	mc=memcache.Client(['127.0.0.1:11211'])
	def make_request():
		compute(mc,random.randint(0,5000))

	print('Ten succesive runs')
	for i in range(1,11):
		print('%.2f s' % timeit.timeit(make_request,number=2000))
	print()

if __name__=='__main__':
	main()
