# -*- coding: utf-8 -*-
'''
import urllib
import urllib.request as request
import urllib.parse as parse
import re 
from bs4 import BeautifulSoup 
from datetime import datetime 
import gzip
import io
import zlib
import unicodedata
import time
import sys
'''
import onedrivesdk 

redirect_uri = 'http://localhost:8080/' 
client_secret = 'Micro0819soft    ' 
client_id='mlvj@outlook.com' 
api_base_url='https://api.onedrive.com/v1.0/' 
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite'] 
http_provider = onedrivesdk.HttpProvider() 
auth_provider = onedrivesdk.AuthProvider( http_provider=http_provider, client_id=client_id, scopes=scopes) 
client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider) 
auth_url = client.auth_provider.get_auth_url(redirect_uri) 

# Ask for the code 
print('Paste this URL into your browser, approve the app\'s access.') 
print('Copy everything in the address bar after "code=", and paste it below.') 
print(auth_url) 
code = raw_input('Paste code here: ') 
client.auth_provider.authenticate(code, redirect_uri, client_secret)

