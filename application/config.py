import os
from collections import defaultdict



class AppConfig :
    
    def __init__(self):
        
        self.apps   = defaultdict(dict)
        self.oidc_rp= defaultdict(dict)

        self.appList = ['okta','test_keycloak','mitreid']
        
        #OKTA
        self.apps[self.appList[0]]['login_form_id'] = 'form17'
        self.apps[self.appList[0]]['login_form_name'] = ''
        self.apps[self.appList[0]]['login_form_username'] = 'okta-signin-username'
        self.apps[self.appList[0]]['login_form_password'] = 'okta-signin-password'
        self.apps[self.appList[0]]['login_form_submit'] = 'okta-signin-submit'
        self.apps[self.appList[0]]['username'] = os.environ['OKTA_USERNAME']
        self.apps[self.appList[0]]['password'] = os.environ['OKTA_PASSWORD']
        
        
        #KEYCLOAK
        self.apps[self.appList[1]]['login_form_id'] = 'form17'
        self.apps[self.appList[1]]['login_form_name'] = ''
        self.apps[self.appList[1]]['login_form_username'] = 'username'
        self.apps[self.appList[1]]['login_form_password'] = 'password'
        self.apps[self.appList[1]]['login_form_submit'] = 'kc-login'
        self.apps[self.appList[1]]['username'] = os.environ['KEYCLOAK_USERNAME']
        self.apps[self.appList[1]]['password'] = os.environ['KEYCLOAK_PASSWORD']
        
        
        #MITREID
        self.apps[self.appList[2]]['login_form_id'] = ''
        self.apps[self.appList[2]]['login_form_name'] = ''
        self.apps[self.appList[2]]['login_form_username'] = 'j_username'
        self.apps[self.appList[2]]['login_form_password'] = 'j_password'
        self.apps[self.appList[2]]['login_form_submit'] = 'submit'
        self.apps[self.appList[2]]['username'] = os.environ['MITREID_USERNAME']
        self.apps[self.appList[2]]['password'] = os.environ['MITREID_PASSWORD']
        
        
        #OIDC RP Docker
        self.oidc_rp[self.appList[0]]['repository'] = os.getcwd() + '/../../server'
        self.oidc_rp[self.appList[1]]['repository'] = os.getcwd() + '/../../server'
        self.oidc_rp[self.appList[2]]['repository'] = os.getcwd() + '/../server'
        
        
        
        self.oidc_rp[self.appList[0]]['tag']  = 'oidc_rp_'  + self.appList[0]
        self.oidc_rp[self.appList[1]]['tag']  = 'oidc_rp_'  + self.appList[1]
        self.oidc_rp[self.appList[2]]['tag']  = 'oidc_rp_'  + self.appList[2]
        
        
    def getAppList(self):
        
        return self.appList
        
        
    def getAppConfig(self,index): 
        return self.apps[self.appList[index]] 
    
    
    def getRpConfig(self,index):
        return self.oidc_rp[self.appList[index]]
    
    
        
