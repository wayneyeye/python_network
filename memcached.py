import memcache
mc=memcache.Client(['127.0.0.1:11211'])
mc.set('user:19','Simple is better than complex.')
print(mc.get('user:19'))
