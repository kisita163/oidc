import requests
import jwt
import json

from oic.oic.message import AuthorizationResponse
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.oauth2.exception import GrantError
from oic.oic import Client
from oic import rndstr
from urllib.parse import urlencode



class Oidc_rp :
    
    
    def __init__(self,client_id,
                 client_secret,
                 client_provider_issuer,
                 client_redirect_uri):
        
        
        self.client = Client(client_authn_method=CLIENT_AUTHN_METHOD,client_id=client_id)
        # client parameters
        self.client.client_secret = client_secret
        self.client.provider_config(client_provider_issuer)
        self.client.redirect_uris = client_redirect_uri
        self.redirect_uri = client_redirect_uri
        
        self.session = {}
    
    def getAuthnRequestUrl(self):
        
        self.session["state"] = rndstr()
        self.session["nonce"] = rndstr()
        args = {
            "response_type": "code",
            "scope": "openid profile",
            "nonce": self.session["nonce"],
            "redirect_uri": self.redirect_uri,
            "state": self.session["state"],
            "client_id": self.client.client_id
        }
        
        auth_req = self.client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request(self.client.authorization_endpoint)
        
        #login_url =  self.client.authorization_endpoint + '?'+ urlencode(args) 
        
        return login_url
    
    def auhtnResponseHandler(self,response):
        error = 0
        code  = ""
        aresp = self.client.parse_response(AuthorizationResponse, info=response,
                              sformat="urlencoded")
        
        try :
            
            state = aresp["state"]
            
            if state != self.session["state"]:
                error = -1
            else:
                code = aresp["code"]
            
        except:
            error = -1
            
        return error,code,state
    
    
    def jwtHandler(self,token_response):
        
        tokens = json.loads(token_response)
        
        
        if 'error' in tokens : 
            return token_response
        
        
        if 'access_token' in tokens :
            access_token = jwt.decode(tokens['access_token'],verify=False)
            tokens['access_token'] = access_token
            print(json.dumps(tokens,indent=2))
        
        if 'id_token' in tokens : 
            id_token = jwt.decode(tokens['id_token'],verify=False)
            tokens['id_token'] = id_token
            print(json.dumps(tokens,indent=2))
        
        return json.dumps(tokens,indent=2)
        
        
    
    
    def doAccessTokenRequest(self,code):
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        args = {
            "code": code,
            "grant_type" : "authorization_code",
            "client_id" : self.client.client_id,
            "client_secret" : self.client.client_secret,
            "redirect_uri":self.redirect_uri
            }
        
        resp = requests.post(self.client.token_endpoint,headers=headers,data=urlencode(args))
        
        response  = self.jwtHandler(resp.content.decode('utf-8'))
        
        return response
            
    def getLastResponse(self):
        return self.last_response


    def doUserInfoRequest(self):
        return self.client.do_user_info_request(state=self.session["state"])
    
