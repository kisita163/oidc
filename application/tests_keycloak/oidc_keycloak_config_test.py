import os
import json
import time

from docker import Client
from oidc_test import BaseAppTest
from keycloak import KeycloakAdmin



class KeycloakBaseTest(BaseAppTest):
    
    def createKeycloakClient(self,config):
                
        print('Creating new oidc client ...')
        keyclaok_id  = self.keycloak_admin.get_client_id(config['name'])
        
        if keyclaok_id is not None : 
            print('Deleting old client...')
            self.keycloak_admin.delete_client(keyclaok_id)
            time.sleep(2)
        else:
            print('This client does not exist yet')
        
        self.keycloak_admin.create_client(config, skip_exists=True)
        return self.keycloak_admin.get_client_id(config['name'])
    
    def getkeycloakClient(self,clientId):
        return self.keycloak_admin.get_client(clientId)
    
    
    
    def deleteKeycloakClient(self,name):   
        
        keyclaok_id  = self.keycloak_admin.get_client_id(name)
        
        if keyclaok_id is not None : 
            self.keycloak_admin.delete_client(keyclaok_id)
            time.sleep(2)
    
    
    def startKeycloakAuthorizationServer(self):
        print('Starting authorization server...')
        #port mapping
        ports = [8080]
        port_bindings = {8080:7010}
        #Environment variables
        environment = ['KEYCLOAK_USER='+os.environ['KEYCLOAK_USERNAME'],
                       'KEYCLOAK_PASSWORD='+os.environ['KEYCLOAK_PASSWORD']]
        #image
        image='jboss/keycloak'
        #Check is not running
        keycloak_status = self.isContainerRunning('http://localhost:7010/auth')
        
        if keycloak_status is not None :
            return
        
        
        host_config = self.client.create_host_config(port_bindings=port_bindings)
    
        container = self.client.create_container(
            image=image,
            ports=ports,
            host_config=host_config,
            environment=environment
        )
        self.client.start(container)
        #Give the container the chance to start
        self.waiContainerRunning('http://localhost:7010/auth')

            
    def stopKeycloakAuthorizationServer(self):
        
        for container in self.client.containers():
            if 'jboss/keycloak' in container['Image']:
                Client().stop(container['Id'])
        
    
    def loadServerConf(self,config):
        
        try : 
            with open(config) as data_file:    
                data = json.load(data_file)
                
        except IOError:
            print('Could not find the server configuration file ('+config+')')
            return None
        
        return data

    def setUp(self):
        
        self.startKeycloakAuthorizationServer()
        super(KeycloakBaseTest,self).setUp()
        self.keycloak_admin = KeycloakAdmin(server_url="http://localhost:7010/auth/",
                                        username=os.environ['KEYCLOAK_USERNAME'],
                                        password=os.environ['KEYCLOAK_PASSWORD'],
                                        realm_name="master",
                                        verify=False)

       
        
    def tearDown(self):
        super(KeycloakBaseTest,self).tearDown()
        self.stopKeycloakAuthorizationServer()
        
        

    
