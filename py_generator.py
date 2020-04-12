def test():
	for i in range(10):
		yield i
	yield 'done'
# make a list
print(list(test()))

# make a list
print([k for k in test()])

# iteration thru
it=test()
print(it)
for k in it:
	print(k)
