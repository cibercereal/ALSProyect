# -*- coding: utf-8 -*-
''' Python AppEngine Sessions 0.1.2
    Felipe A. Hernandez
    spayder26 at gmail dot com

    ***
    Licensed under General Public License version 3 Terms:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    ***

    Usage:
    You need to initialize a Session object, on every request, giving
    the current RequestHandler instance for proper Cookie handling.
    Session instance's write method must be invoked before request
    finished and data was send to client.
    
    Classes:
    * DataDict:
        A simple serializable dictionary without KeyErrors. It returns
        None when key was not found). It has also a flag (changed),
        which is setted to true when a item is setted. If you modify
        an inner object, you must set "changed" flag to true manually.
        
    * Session:
        Abstraction layer for two DataDicts, one for server and another
        for a client, and Session-cookie interface.
        It's dictionary-like, keys prefixed with an underscore ("_")
        will be stored on server, anyelse will be encrypted and stored
        on client's browser as a cookie.
        So be carefull storing sensible data on client.
        Methods:
        * __getitem__ and __setitem__
            Methods for dictionary like behavior. You can access sesion
            data directly, prefixing underscore ("_") for server data
            on keys' names.
        * write
            This metod must be invoked before request's ending to save
            session cookies on http headers. 
            
    Example:
    from google.appengine.ext.webapp.util import run_wsgi_app
    from google.appengine.ext import webapp
    from appSession import Session

    class RequestWeb(webapp.RequestHandler):
        def get(self):
            session = Session(self, debug=True)

            if session["visited"]:
                text = "Times visited %d." % session["visited"]
                session["visited"] += 1
            else:
                text = "First time on page."
                session["visited"] = 1
                    
            session["_foo"] = "This string will be stored on server."
            session["bar"] = "This string will be stored on a cookie."
            
            session.write()
            self.response.out.write(
                "<html><head></head><body><p>%s</p></body></html>" % text
                )

    application = webapp.WSGIApplication([
        ('/',RequestWeb)
        ],
        debug=True)

    run_wsgi_app(application)
'''

__all__ = ["DataDict","Session"]
__author__ = "Felipe A. Hernandez"
__authemail__ = "spayder26 at gmail dot com"
__version__ = "0.1.2"
__license__ = "GPLv3"

import logging
from google.appengine.api import memcache
from base64 import b64encode as encode, b64decode as decode
from random import sample

from PRSerializer import dumps as dump, loads as load, register as serializable

from appCrypto import Crypto as Encryptor

from sys import version_info as python_version
if python_version < (2,6): from Cookie26 import BaseCookie
else: from Cookie import BaseCookie

class SessionCookie(BaseCookie):
    '''BaseCookie wrapper'''
    def append(self, key, value, HttpOnly = False,
    httponly = False, max_age = None, path = None, domain = None,
    secure = None, version = None, comment = None):
        '''Simple interface to add a cookie.'''
        self.__setitem__(key, value)
        if max_age is not None:
            self.__getitem__(key).__setitem__('expires', str(max_age))  
        for var_name, var_value in [
            ('max-age', max_age),
            ('path', path),
            ('domain', domain),
            ('secure', secure),
            ('HttpOnly', HttpOnly or httponly), # Only available on 2.6
            ('version', version),
            ('comment', comment),
            ]:
            if not var_value in (None, False):
                self.__getitem__(key).__setitem__(var_name, str(var_value))

    def __str__(self):
        return "<SessionCookie %s>" % repr(self.output())
      
class DataDict(dict):
    '''A dictionary with a public 'changed' boolean flag, without
    KeyErrors (return None if key not found) and items will be removed
    if None is asigned, serializable by PRSerializer.
    '''
    
    changed = False
    
    def __getstate__(self):
        return dict(self) # Pickles as dict
        
    def __setstate__(self, d):
        '''Serialization set method. See `PRSerializer`.'''
        return self.__init__(d)
    
    def __getitem__(self, key):
        '''Serialization get method. See `PRSerializer`.'''
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        return None
    
    def __setitem__(self, key, value):
        '''x.__setitem__(i, y) <==> x[i]=y'''
        if value == None:
            self.__delitem__(key)
        else:
            dict.__setitem__(self, key, value)
            self.changed = True
        
    def __delitem__(self, key):
        '''x.__getitem__(y) <==> x[y]'''
        if dict.__contains__(self, key):
            dict.__delitem__(self, key)
            self.changed = True
serializable(DataDict)

class Session(object):
    '''Session class, required to be initialized with a request handler
    and write() method must be exec before sending content to client'''
    
    # Session data
    __crypt = None # Initialized cryptographic class
    __sid = None # Session id
    __isnew = False # If session was created on this request
    __clientvars = None # Client data dictionary
    __servervars = None # Server data dictionary
    
    # Sid generator settings
    __sid_length = 64
    __sid_chars = ('0123456789' +
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                   'abcdefghijklmnopqrstuvwxyz' +
                   "!#$%&'*+-.^_`|~")
    __sid_chars_length = len(__sid_chars)
    
    # Cookies config
    __cookie_sid  = "-session"
    __cookie_data = "-session-data"
    
    # Memcache namespace
    __memcache_namespace = "-session"
    
    # Convenience request and response instances
    request = None
    response = None
    
    def __gensid__(self, length = None):
        ''' Generates the session ID
        
        Arguments:
            length: the length of the generated id
        
        Return:
            Random id with given length.'''
        if not length:
            length = self.__sid_length
        return "".join( sample( self.__sid_chars*length, length) )
        
    def __encrypt__(self, data):
        '''Serialize and encrypt object.
        
        Arguments:
            data: object will be serialized and encrypted.
            
        Returns:
            Encrypted serialized string.
        '''
        return encode( self.__crypt.encrypt( dump( data , -1 ) ) )
        
    def __decrypt__(self, data):
        '''Decrypt and unserialize object
        
        Arguments:
            data: str object of encrypted serialized data
            
        Returns:
            Unserialized object.'''
        try:
            return load( self.__crypt.decrypt( decode( data ) ) )
        except UnpicklingError:
            return None
            
    def __memget__( self, sid, namespace = None ):
        '''Serialization get method. See `PRSerializer`.'''
        if isinstance(sid, list): pass
        return memcache.get(
            sid,
            namespace=(
                namespace or self.__memcache_namespace
                )
            )
        
    def __memset__(self, sid, data=None, namespace = None):
        '''Serialization set method. See `PRSerializer`.'''
        if isinstance(sid, dict):
            pass
        elif data:
            memcache.set(
                sid,
                data,
                namespace=(
                    namespace or self.__memcache_namespace
                    ),
                time=self.__memtime,
                )
    
    def __init__(self, requestHandler, time = 3600, path = "/", cookie_prefix = "app", debug = False):
        '''Session initialization, reads from request cookies and looks
        for session cookies. Then, theyre are decrypted and validated
        against memcache.
        
        This object supports key indexing (__getitem__ and __setitem__)
        and the *in* operator.
        
        Arguments:
            requestHandler: Appengine or wsgi compatible handler
                            instance.
            time: Memcache data expiration time. Defaults to 3600.
            path: Cookie domain path. Defaults to "/".
            cookie_prefix: string will be used prefixing cookie names.
                           Defaults to "app".
            debug: print logging messages on write. Defaults to False.

        '''

        self.__clientvars = DataDict()
        self.__servervars = DataDict()
        self.__path = path
        self.__memtime = time
        self.__cookie_prefix = cookie_prefix
        
        self.debug = debug
        self.request = requestHandler.request
        self.response = requestHandler.response
        
        cookiesid = "%s%s" % (cookie_prefix, self.__cookie_sid)
        cookiedata = "%s%s" % (cookie_prefix, self.__cookie_data)
        
        cookies = SessionCookie( self.request.headers.get('Cookie') )  
        if (cookiesid in cookies) and \
           (cookiedata in cookies):
            # Cookies
            c = cookies[ cookiesid ]
            d = cookies[ cookiedata ]

            # Requesting server-side session data
            sdata = self.__memget__( c.value )
            if isinstance(sdata, DataDict):
                # New encryptor with server key
                #try:
                self.__crypt = Encryptor( sdata["key"], sdata["encryption"] )
                # Decrypting the cookie data
                cdata = self.__decrypt__( d.value )
                if isinstance(cdata, DataDict):
                    if self.debug:
                        logging.info("Session id: %s" % repr(c.value) )
                        logging.info("Client data: %s" % repr(cdata) )
                        logging.info("Server data: %s" % repr(sdata) )
                        # TODO: Validating cookie data

                    # If everything is correct, we accept the data
                    self.__sid = c.value
                    self.__clientvars = cdata
                    self.__servervars = sdata
                '''except:
                    # Ban behavior
                    pass'''

        if self.__sid == None:
            logging.info("no cookie")
            self.__isnew = True
            self.__sid = self.__gensid__()  # New session id
            self.__crypt = Encryptor() # New encryptor
            self.__servervars["key"] = self.__crypt.key # Save key on server
            self.__servervars["encryption"] = self.__crypt.algorithm # Remember algorithm
            
    def __setitem__(self, key, value):
        '''x.__setitem__(i, y) <==> x[i]=y'''
        if key[0]=="_": self.__servervars.__setitem__(key, value)
        else: self.__clientvars.__setitem__(key, value)
        
    def __getitem__(self, key):
        '''x.__getitem__(y) <==> x[y]'''
        if key[0]=="_": return self.__servervars.__getitem__(key)
        return self.__clientvars.__getitem__(key)
    
    def __contains__(self, key):
        '''D.__contains__(k) -> True if D has a key k, else False'''
        if key[0]=="_":
            return self.__servervars.__contains__(key)
        return self.__clientvars.__contains__(key)
    
    def write(self):
        '''Writes session cookies on response object's headers.'''
        if self.__servervars.changed:
            # Server side data
            self.__memset__( self.__sid, self.__servervars )
    
        # We create an up-to-date SessionCookie from request headers
        cookies = SessionCookie() #self.request.headers.get('Cookie') )
        
        if self.__isnew:
            if self.debug: logging.info("setted %s%s" % (self.__cookie_prefix, self.__cookie_sid))
            # Client side session id
            cookies.append(
                "%s%s" % (self.__cookie_prefix, self.__cookie_sid),
                self.__sid,
                HttpOnly = True,
                path = self.__path,
                )
        
        if self.__isnew or self.__clientvars.changed:
            if self.debug: logging.info("setted %s%s" % (self.__cookie_prefix, self.__cookie_data))
            # Client side data
            cookies.append(
                "%s%s" % (self.__cookie_prefix, self.__cookie_data),
                self.__encrypt__(self.__clientvars),
                HttpOnly = True,
                path = self.__path,
                )

        for morsel in cookies.values():
            self.response.headers.add_header('Set-Cookie', morsel.OutputString(None))
