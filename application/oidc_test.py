import unittest
import time


from docker import Client
from config import AppConfig
from selenium import webdriver


class BaseAppTest(unittest.TestCase) : 
    
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

        #New docker client
        self.client = Client()
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
        for n in range(0,9) : 
            print('*')
            time.sleep(1)
            
            
    def stopOidcRp(self):
        
        print('Stopping ' + self.oidc_rp_id )
        self.client.stop(self.oidc_rp_id)
        self.client.close()
            
            
    def setUp(self):
        self.driver    = webdriver.Firefox()
        
        
    def tearDown(self):
        self.driver.close()
        self.stopOidcRp()   
        
        