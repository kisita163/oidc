import unittest
import requests
import json
import time
import pytest
from docker import Client
from config import AppConfig
from selenium import webdriver

from oidc_test import BaseAppTest

from selenium.common.exceptions import TimeoutException, NoSuchElementException



class TestOidcOkta(BaseAppTest):
    
    def setUp(self):
        #OIDC Provider
        self.index = 0
        self.startOidcRp(self.index)
        super().setUp()
        

    def test_authz_requet_url(self):
        
        print('Start test_authz_requet_url')
        
        response = requests.get('http://localhost:7011/authorization-request/url')
        
        self.assertIn('redirect_uri=http', response.text)
        self.assertIn('response_type', response.text)
        self.assertIn('client_id', response.text)
        self.assertIn('scope', response.text)
    

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
        
        time.sleep(10)
        
        response = requests.get('http://localhost:7011/getLastResponse')
        
        time.sleep(5)
        
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
        
        
        
if __name__ == "__main__":
    unittest.main()
