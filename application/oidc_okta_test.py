import unittest
import requests
import json
import time
from docker import Client
from config import AppConfig
from selenium import webdriver

from selenium.common.exceptions import TimeoutException, NoSuchElementException



class TestOidcOkta(unittest.TestCase):
    
    def startOidcRp(self):
        #port mapping
        ports = [7011]
        port_bindings = {7011: 7011}
        #Environment variables
        environment = ['CONFIG='+str(self.index)]

        #New docker client
        self.client = Client()
        #Build the container
        path = self.appConfig.getRpConfig(self.index)['repository']
        tag  = self.appConfig.getRpConfig(self.index)['tag']
          
        output  = self.client.build(path=path, 
                                    tag=tag) 
        #New container logs
        for t in output : print(t)
        assert('Successfully' in str(t))
        
        
        host_config = self.client.create_host_config(port_bindings=port_bindings)

        container = self.client.create_container(
            image=tag,
            ports=ports,
            host_config=host_config,
            environment=environment
        )
        self.client.start(container)
        
        self.oidc_rp_id = container['Id']
        
        print('Starting container ' + self.oidc_rp_id)
        #Give the container the chance to start
        for n in range(0,9) : 
            print('*')
            time.sleep(1)
    
    def stopOidcRp(self):
        print('Stopping ' + self.oidc_rp_id )
        self.client.stop(self.oidc_rp_id)
        self.client.close()
    
    

    def setUp(self):
        #OIDC Provider
        self.index = 0
        self.appConfig = AppConfig()
        self.startOidcRp()
        self.driver    = webdriver.Firefox()
        

    def test_authz_requet_url(self):
        
        print('Start test_authz_requet_url')
        
        response = requests.get('http://localhost:7011/authorization-request/url')
        
        self.assertIn('redirect_uri=http', response.text)
        self.assertIn('response_type', response.text)
        self.assertIn('client_id', response.text)
        self.assertIn('scope', response.text)
        
        print(response.text)
    
    
    

    def login(self):
        #Return value
        status = True
        # Get Authentication URL from OP
        response = requests.get('http://localhost:7011/authorization-request/url')
        self.driver.get(response.text)
        print(response.text)
        
        
        time.sleep(5)
        try:
            self.driver.find_element_by_id(self.appConfig.getAppConfig(self.index)['login_form_username']).send_keys(self.appConfig.getAppConfig(self.index)['username'])
            self.driver.find_element_by_id(self.appConfig.getAppConfig(self.index)['login_form_password']).send_keys(self.appConfig.getAppConfig(self.index)['password'])
            self.driver.find_element_by_id(self.appConfig.getAppConfig(self.index)['login_form_submit']).click()
            
        except NoSuchElementException:
            status = False
            pass
            
            
        return status

    def test_login_screen(self): 
        
        print('Start test_login_screen')
        
        assert(self.login())
        
        
     
    def test_access_token(self):   
        
        assert(self.login())
        
        time.sleep(5)
        
        response = requests.get('http://localhost:7011/getLastResponse')
        
        time.sleep(1)
        
        resp = response.text
        resp = resp.replace("\'", "\"")
        resp = json.loads(resp)
        
        print("")
        print(json.dumps(resp,indent=2))
        print("")
        self.assertIn('access_token', response.text)
        self.assertIn('token_type', response.text)
        self.assertIn('expires_in', response.text)
        self.assertIn('scope', response.text)
        self.assertIn('id_token', response.text)
        self.assertIn('nationalRegistryNumber', response.text)
        

    def tearDown(self):
        self.driver.close()
        self.stopOidcRp()
       
        
        
if __name__ == "__main__":
    unittest.main()
