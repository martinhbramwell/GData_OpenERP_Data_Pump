#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-11-25

@author: Martin H. Bramwell
'''
from persistence import store, close_store, make_store, reopen_store
from gspread import login, authorize

store = None
if not store :
    store = make_store()
    
expr = "Missing or misformed configuration file(s)."
msg = "Either a file named 'creds_oa.py' or a file named 'creds_up.py' must be present in order to authenticate your connection to Google."

credentials = {}
try:
    credentials = store['credentials']
except KeyError:
    try:
        from creds_oa import credentials
        print "Will connect with gspread.authorize()"
    except ImportError:
        try:
            from creds_upx import credentials
            print "Will connect with gspread.login()"
        except ImportError:
            print "Configuration error: {} {}".format(expr, msg)
            exit(-1)

    store['credentials'] = credentials
    reopen_store()
    print "The creds_*.py file(s) may now be deleted."

OAUTH = "oauth"
UID_PWD = "uidpwd"

class GoogleConnection(object):

    connection = "nuthin'"

    if credentials['cred_type'] == OAUTH:
        connection = authorize(credentials['access_token'], credentials['key_ring'])
    elif credentials['cred_type'] == UID_PWD:
        connection = login(credentials['uid'], credentials['pwd'])
    else:
        print "Configuration error: {} {}".format(expr, msg) 
        exit(-1)

        
