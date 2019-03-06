import unittest
import requests
import json
import time
import pytest

from oidc_test import BaseAppTest


from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from jsonschema._utils import indent



class TestOidcMitreid(BaseAppTest):
    
    def setUp(self):
        self.index = 2
        self.startOidcRp(self.index)
        super().setUp()
    

    @pytest.mark.order1
    def test_authz_requet_url(self):
        
        print('Start test_authz_requet_url')
        
        response = requests.get('http://localhost:7011/authorization-request/url')
        
        authz_req_url = response.text
        
        self.assertIn('redirect_uri=http',authz_req_url)
        self.assertIn('response_type',authz_req_url)
        self.assertIn('client_id',authz_req_url)
        self.assertIn('scope', authz_req_url)
        
        
        
        print(response.text)
    
    
    @pytest.mark.order2
    def test_login_screen(self): 
        
        print('Start test_login_screen ')
        
        response = requests.get('http://localhost:7011/authorization-request/url')
        #
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
       
        
        
if __name__ == "__main__":
    unittest.main()