import urllib.request


try :
    urllib.request.urlopen('http://localhost:7010/auth')
    print('done')
except: 
    print('not done')
    


urllib.request.urlopen('http://localhost:7010/auth')