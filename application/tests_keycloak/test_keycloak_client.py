import unittest
import json

from tests_keycloak.oidc_keycloak_config_test import KeycloakBaseTest


class TestOidcClientKeycloak(KeycloakBaseTest):
    
    def setUp(self):
        KeycloakBaseTest.setUp(self)
        self.client_name  = 'client_test'
        self.client_id    = 'client_test'
        
        
    def test_new_client(self):
        keycloak_config  = self.loadServerConf('keycloak_client.json')
        
        keycloak_config['name']     = self.client_name
        keycloak_config['clientId'] = self.client_id
        keycloakClientId = self.createKeycloakClient(keycloak_config)
        
        keycloakClient   = self.getkeycloakClient(keycloakClientId)
        
        
        print(json.dumps(keycloakClient,indent=2))
        self.assertEqual(keycloakClient['name'],self.client_name)
        
        
    def test_create_client_scope(self):
        
        keycloak_config  = self.loadServerConf('keycloak_client.json')
        keycloakClientId = self.createKeycloakClient(keycloak_config)
        
        keycloakClient   = self.getkeycloakClient(keycloakClientId)
        
        
        print(json.dumps(keycloakClient,indent=2))
        assert(True)
        
       
        
    def tearDown(self):
        self.deleteKeycloakClient(self.client_name)
        KeycloakBaseTest.tearDown(self)
        
        


if __name__ == "__main__":
    unittest.main()