from collections import defaultdict



class AppConfig :
    
    def __init__(self):
        
        self.apps   = defaultdict(dict)
        self.oidc_rp= defaultdict(dict)

        self.appList = ['okta','keycloak','mitreid']
        
        #OKTA
        self.apps[self.appList[0]]['login_form_id'] = 'form17'
        self.apps[self.appList[0]]['login_form_name'] = ''
        self.apps[self.appList[0]]['login_form_username'] = 'okta-signin-username'
        self.apps[self.appList[0]]['login_form_password'] = 'okta-signin-password'
        self.apps[self.appList[0]]['login_form_submit'] = 'okta-signin-submit'
        self.apps[self.appList[0]]['username'] = 'hugues.kisitankebi@belfius.be'
        self.apps[self.appList[0]]['password'] = '************'
        
        
        #KEYCLOAK
        self.apps[self.appList[1]]['login_form_id'] = 'form17'
        self.apps[self.appList[1]]['login_form_name'] = ''
        self.apps[self.appList[1]]['login_form_username'] = 'username'
        self.apps[self.appList[1]]['login_form_password'] = 'password'
        self.apps[self.appList[1]]['login_form_submit'] = 'kc-login'
        self.apps[self.appList[1]]['username'] = 'hugues.kisitankebi@belfius.be'
        self.apps[self.appList[1]]['password'] = '************'
        
        
        #MITREID
        self.apps[self.appList[2]]['login_form_id'] = ''
        self.apps[self.appList[2]]['login_form_name'] = ''
        self.apps[self.appList[2]]['login_form_username'] = 'j_username'
        self.apps[self.appList[2]]['login_form_password'] = 'j_password'
        self.apps[self.appList[2]]['login_form_submit'] = 'submit'
        self.apps[self.appList[2]]['username'] = 'admin'
        self.apps[self.appList[2]]['password'] = 'password'
        
        
        #OIDC RP Docker
        self.oidc_rp[self.appList[0]]['repository'] = '/home/firebase/server/'+ self.appList[0]
        self.oidc_rp[self.appList[1]]['repository'] = '/home/firebase/server/'+ self.appList[0]
        self.oidc_rp[self.appList[2]]['repository'] = '/home/firebase/server/'+ self.appList[0]
        
        
        
        self.oidc_rp[self.appList[0]]['tag']  = 'oidc_rp_'  + self.appList[0]
        self.oidc_rp[self.appList[1]]['tag']  = 'oidc_rp_'  + self.appList[1]
        self.oidc_rp[self.appList[2]]['tag']  = 'oidc_rp_'  + self.appList[2]
        
        
    def getAppList(self):
        
        return self.appList
        
        
    def getAppConfig(self,index): 
        return self.apps[self.appList[index]] 
    
    
    def getRpConfig(self,index):
        return self.oidc_rp[self.appList[index]]
    
    
        
