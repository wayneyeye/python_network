import requests
# get request headers
r=requests.get('http://httpbin.org/headers')
print(r.text)

# status code
r=requests.get('http://httpbin.org/status/301')
print(r.status_code,r.url)
print(r.history)

# disables the redirection
r=requests.get('http://httpbin.org/status/301',allow_redirects=False)
r.raise_for_status()
print(r.status_code, r.url,r.headers)
print(r.text)

r=requests.get('http://google.com',allow_redirects=False)
r.raise_for_status()
print(r.status_code, r.url,r.headers)
print(r.text)

r=requests.get('http://httpbin.org/redirect/1',allow_redirects=False)
r.raise_for_status()
print(r.status_code, r.url,r.headers)
print(r.text)

# http auth
r=requests.get('http://httpbin.org/headers',auth=('wayne','qwert12345'))
print(r.text)

