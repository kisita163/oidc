import unittest
import requests
import json
import time
from docker import Client
from application.config import AppConfig
from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from jsonschema._utils import indent



class TestOidcOkta(unittest.TestCase):
    
    def startOidcRp(self):
        #port mapping
        ports = [8080]
        port_bindings = {8080: 7011}
        #Environment variables
        environment = ['CONFIG='+str(self.index)]
        #Network mode
        network_mode='host'

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
        
        
        host_config = self.client.create_host_config(port_bindings=port_bindings,
                                                     network_mode=network_mode)
        
        container = self.client.create_container(
            image=tag,
            ports=ports,
            host_config=host_config,
            environment=environment,
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
        self.index = 2
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
    
    
    
    def test_login_screen(self): 
        
        print('Start test_login_screen')
        
        response = requests.get('http://localhost:7011/authorization-request/url')
        #start the browser with the provider URL
        self.driver.get(response.text)
        
        print(response.text)
 
        try:
            self.driver.find_element_by_id(self.appConfig.getAppConfig(self.index)['login_form_username']).send_keys(self.appConfig.getAppConfig(self.index)['username'])
            self.driver.find_element_by_id (self.appConfig.getAppConfig(self.index)['login_form_password']).send_keys(self.appConfig.getAppConfig(self.index)['password'])
            self.driver.find_element_by_name(self.appConfig.getAppConfig(self.index)['login_form_submit']).click()
            
            
            authorize_present = EC.presence_of_element_located((By.NAME, 'authorize'))
            WebDriverWait(self.driver, 5).until(authorize_present)
            self.driver.find_element_by_name('authorize').click()
            
        except TimeoutException:
            print("Timed out waiting for page to load")
        
 
        time.sleep(5)
        
        response = requests.get('http://localhost:7011/getLastResponse')
        
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
        


    def tearDown(self):
        self.driver.close()
        self.stopOidcRp()
       
        
        
if __name__ == "__main__":
    unittest.main()