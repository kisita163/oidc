import json
import os

from flask import Flask
from flask import request
from oidc_rp import Oidc_rp

app = Flask(__name__)


@app.route('/authorization-request/url')
def getAuthnUrl():
    return rp.getAuthnRequestUrl()

@app.route('/authorization-code/callback')
def handleAuthzCode():
    
    response = '{error : \'Failed to get tokens from OIDC provider\'}'
    error,code,state = rp.auhtnResponseHandler(request.url)
    
    if error == 0 :
        response = rp.doAccessTokenRequest(code)
        
    return str(response)

@app.route('/userinfo')
def getUserInfo():
    return str(rp.doUserInfoRequest())

@app.route('/getLastResponse')
def getLastResponse():
    return str(rp.getLastResponse())


def loadServerConf(config):
    
    try : 
        with open(config) as data_file:    
            data = json.load(data_file)
            
    except IOError:
        print('Could not find the server configuration file ('+config+')')
        return None
    
    return data

if __name__ == '__main__':
    
    server_data = loadServerConf('config.json')
   
    if server_data is not None :
        conf = int(os.environ['CONFIG'])
        rp  = Oidc_rp(server_data[conf]['client_id'],
                      server_data[conf]['client_secret'],
                      server_data[conf]['issuer'],
                      server_data[conf]['redirect_uri'])
        
        app.run(host='0.0.0.0',port=7011, debug=True)
    
