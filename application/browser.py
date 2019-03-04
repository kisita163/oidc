import mechanize
from mechanize import HTTPError
from mechanize._form_controls import ControlNotFoundError
from mechanize._mechanize import FormNotFoundError


class Browser : 
    
    def __init__(self):
        self.browser       = mechanize.Browser()
        self.browser.set_handle_redirect(False)
        self.browser.set_debug_http(False)
        self.browser.set_handle_robots(False)
        
        self.header = None
        self.body   = None
        self.code   = None
        
        
            
    
    def clientBrowser(self,url,
                      username=None,
                      password=None,
                      consent=False,
                      data_to_send=None,
                      form_id=None,
                      form_username=None,
                      form_password=None):
        try:
            self.browser.open(url,data=data_to_send)
            
            if username is not None :
                if password is not None :
                    if form_id is not None :
                        self.browser.select_form(id=form_id)
                         
                        for f in self.browser.forms():
                            print f.name
                            
                        self.browser.form[form_username] = username
                        self.browser.form[form_password] = password
                        self.browser.submit()
                    
            if consent is True : 
                    self.browser.select_form(name='confirmationForm')
                    self.browser.submit(name='authorize')
                

        except HTTPError:
            print 'HTTPError'
            pass
        
        except ControlNotFoundError : 
            print 'ControlNotFoundError'
            pass
        
        except FormNotFoundError:
            print 'FormNotFoundError...'
            pass
        
            
        self.header = self.browser.response().info()
        self.code   = self.browser.response().getcode()  
        self.body   = self.browser.response().read()       
    
    def request(self,url,data=None,headers={}):
        
        request = mechanize.Request(url,data,headers)
        
        try :
            self.browser.open(request)
            
        except HTTPError:
            pass
        
        
        self.header = self.browser.response().info()
        self.code   = self.browser.response().getcode()  
        self.body   = self.browser.response().read()
        

    
    def getHeader(self):
        return self.header
    
    def getBody(self):
        return self.body
    
    def getCode(self):
        return self.code
