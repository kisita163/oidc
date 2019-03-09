import unittest
import requests
import urllib.request
import time


from docker import Client
from config import AppConfig
from selenium.common.exceptions import NoSuchElementException



class BaseAppTest(unittest.TestCase) : 
    
    def __init__(self, *args, **kwargs):
        super(BaseAppTest, self).__init__(*args, **kwargs)
        #New docker RP client
        self.client = Client()
        self.oidc_rp_id = None
        
    def isAuthServerUp(self,server):
        
        try :
            urllib.request.urlopen(server)
            return True
        except: 
            return False
    
    def isContainerRunning(self,name):
        
        if not isinstance(name,str):
            return None
        
        if self.isAuthServerUp(name):
            return name
    
        return None
    
    def waiContainerRunning(self,name,timeout=3600):
      
        started = 0
        status  = False
        
        print('Waiting for ' + name)
        
        while(True):
            if self.isContainerRunning(name) is None :
                started = started + 1
                time.sleep(1)
                print(name + ' is not running ('+str(started)+')')
                if started == timeout : 
                    print(name + ' is not running. Leaving the loop...')
                    break 
            else :
                print(name + ' is running.')
                status = True
                break
        
        return status

        
    
    def startOidcRp(self,index):
        #OIDC Provider configuration
        self.appConfig = AppConfig()
        #port mapping
        ports = [7011]
        port_bindings = {7011: 7011}
        #Environment variables
        environment = ['CONFIG='+str(index),'TZ=America/Los_Angeles']
        #Network mode
        network_mode='host'
        #Build the container
        path = self.appConfig.getRpConfig(index)['repository']
        tag  = self.appConfig.getRpConfig(index)['tag']
        
          
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
            environment=environment
        )
        self.client.start(container)
        
        self.oidc_rp_id = container['Id']
        
        print('Starting container ' + self.oidc_rp_id)
        #Give the container the chance to start
        self.waiContainerRunning('http://localhost:7011/home')
            
            
    def login(self,index):
        #Return value
        status = True
        # Get Authentication URL from OP
        response = requests.get('http://localhost:7011/authorization-request/url')
        self.driver.get(response.text)
        print(response.text)
        
        
        time.sleep(5)
        try:
            self.driver.find_element_by_id(self.appConfig.getAppConfig(index)['login_form_username']).send_keys(self.appConfig.getAppConfig(index)['username'])
            self.driver.find_element_by_id(self.appConfig.getAppConfig(index)['login_form_password']).send_keys(self.appConfig.getAppConfig(index)['password'])
            self.driver.find_element_by_id(self.appConfig.getAppConfig(index)['login_form_submit']).click()
            
        except NoSuchElementException:
            status = False
            pass
            
            
        return status
            
            
    def stopOidcRp(self):
        
        if self.oidc_rp_id is not None : 
            print('Stopping ' + self.oidc_rp_id )
            self.client.stop(self.oidc_rp_id)
        self.client.close()
            
        
        
    def tearDown(self):
        self.stopOidcRp()   
        
        