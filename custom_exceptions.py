class DestinationError(Exception):
	def __str__(self):
		#return "%s" %(self.args[0]+'abc')
		return '%s-->%s with context %s' % (self.args[0], self.__cause__,self.__context__)

try:
	1/0
except ZeroDivisionError as e:
	#raise DestinationError('Error!!!') # raise another exception during error handling
	raise DestinationError('DestinationError caused by ') from None # eliminate the context
	#raise DestinationError('DestinationError caused by ') from e # set a direct causal relation ship

