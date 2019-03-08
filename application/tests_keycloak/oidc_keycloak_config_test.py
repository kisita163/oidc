import os
import json
import time


from docker import Client
from keycloak import KeycloakAdmin
from oidc_test import BaseAppTest



class KeycloakBaseTest(BaseAppTest):
    
    def startKeycloakAuthorizationServer(self):
        #port mapping
        ports = [8080]
        port_bindings = {8080:7010}
        #Environment variables
        environment = ['KEYCLOAK_USER='+os.environ['KEYCLOAK_USERNAME'],
                       'KEYCLOAK_PASSWORD='+os.environ['KEYCLOAK_PASSWORD']]
        #image
        image='jboss/keycloak:latest'
        #New docker client
        client = Client()
            
        
        host_config = client.create_host_config(port_bindings=port_bindings)
    
        container = client.create_container(
            image=image,
            ports=ports,
            host_config=host_config,
            environment=environment
        )
        client.start(container)
        
        self.oidc_rp_id = container['Id']
        
        print('Starting container ' + self.oidc_rp_id)
        #Give the container the chance to start

            
    def stopKeycloakAuthorizationServer(self):
        
        container_id = self.isContainerRunning('keycloak')
        
        if container_id is not None :
            Client().stop(container_id)
        
    
    def loadServerConf(self,config):
        
        try : 
            with open(config) as data_file:    
                data = json.load(data_file)
                
        except IOError:
            print('Could not find the server configuration file ('+config+')')
            return None
        
        return data


    
