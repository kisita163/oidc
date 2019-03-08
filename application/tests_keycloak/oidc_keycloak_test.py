import unittest
import requests
import json
import time

from oidc_test import BaseAppTest




class TestOidcKeyCloak(BaseAppTest):
    
    #docker run -e KEYCLOAK_USER= -e KEYCLOAK_PASSWORD=password -p 7010:8080 --detach jboss/test_keycloak
    
    def setUp(self):
        #OIDC Provider
        self.index = 1
        self.startOidcRp(self.index)
        super(TestOidcKeyCloak,self).setUp()
        
    
    def test_authz_request_url(self):
        
        print('Testing authorization request URL ...')
        
        response = requests.get('http://localhost:7011/authorization-request/url')
        
        self.assertIn('redirect_uri=http', response.text)
        self.assertIn('response_type', response.text)
        self.assertIn('client_id', response.text)
        self.assertIn('scope', response.text)
        
    def test_login_screen(self): 
        
        print('Start test_login_screen')
        
        assert(self.login(self.index))
        
        
    def test_access_token_with_custom_claim(self):   
        
        assert(self.login(self.index))
        
        time.sleep(2)
        
        response = requests.get('http://localhost:7011/getLastResponse')
        
        time.sleep(2)
        
        resp = response.text
        resp = json.loads(resp)
        
        print("")
        print(json.dumps(resp,indent=2))
        print("")
        self.assertIn('access_token', response.text)
        self.assertIn('token_type', response.text)
        self.assertIn('expires_in', response.text)
        self.assertIn('scope', response.text)
        self.assertIn('id_token', response.text)
     
       
        
        
if __name__ == "__main__":
    unittest.main()