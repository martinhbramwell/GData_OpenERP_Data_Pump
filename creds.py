#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''

import os
import json
import argparse
import errno

credential_file = '.gdataCreds'
credential_path = os.path.expanduser('~') + '/' + credential_file
allow_to_overwrite_prior_credentials = True

NONE = -1
USER_ID = NONE + 1
USER_PWD = USER_ID + 1
START_ROW = USER_PWD + 1

SHORT = NONE + 1
LONG = SHORT + 1
HELP = LONG + 1
switches = [
              ['u', '--user_id', 'Name of the connecting user.']
            , ['p', '--user_pwd', 'Password of the connecting user.']
            , ['r', '--start_row', 'Row in Tasks sheet at which to start processing .']
           ]

class InputError(Exception):
    """ Exception raised for errors in the input.
    Attributes:
        expr -- input expression in which the error occurred
        msg -- explanation of the error
    """
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


def init(credentialFile):
    credential_path = credentialFile

def load():

    creds = None
    try:
        with open(credential_path, 'rb') as fileCredentials:
            creds = json.load(fileCredentials)
    except IOError:
        print "Found no credentials file : '" + credential_path + "'.  Creating now ..."

    return creds

def save(creds):

    with open(credential_path, 'wb') as fileCredentials:
        json.dump(creds, fileCredentials)

    return

def get():

    global allow_to_overwrite_prior_credentials
    
    temp = {}
#    credentials['user_id'] = None
    #credentials['user_pwd'] = None
    
    parser = argparse.ArgumentParser(description='Helper to initialize Google uid/pwd logins')
    parser.add_argument('-' + switches[START_ROW][SHORT], switches[START_ROW][LONG], help = switches[START_ROW][HELP])
    parser.add_argument('-' + switches[USER_PWD][SHORT], switches[USER_PWD][LONG], help = switches[USER_PWD][HELP])
    parser.add_argument('-' + switches[USER_ID][SHORT], switches[USER_ID][LONG], help = switches[USER_ID][HELP])
    
    parser.add_argument('key', help = 'A Google Spreadsheet key')
    
    args = parser.parse_args()
    temp['user_id'] = args.user_id
    temp['user_pwd'] = args.user_pwd
    
#        credentials['user_id'] = args.user_id
#        credentials['user_pwd'] = args.user_pwd


    credentials = load()
    if credentials is None:
        credentials = temp
        save(credentials)
    elif temp['user_id'] is not None and temp['user_pwd'] is not None:
        answer = {
                  '1':'Overwrote prior credentials.'
                , '2':'Using provided command line options without saving.'
                , '3':'Ignoring command line options and using stored ones.'}
        print 'Prior credentials were found in : ' + credential_path
        print '1) Overwrite prior credentials?'
        print '2) Use provided credentials just this time?'
        print '3) Ignore provided credentials?'
        choice = ' (1/2/3)  '
        inp = raw_input(choice)
        while inp not in ('1', '2', '3') :
            print 'invalid input'
            inp = raw_input(choice)
        print answer[inp]
        allow_to_overwrite_prior_credentials = True
        if (inp != '3'):
            credentials = temp
            if (inp != '2'):
                save(credentials)
            else:
                allow_to_overwrite_prior_credentials = False
    
    credentials['key'] = args.key
    credentials['row'] = args.start_row
    return credentials


def silentremove(filename):
    
    if allow_to_overwrite_prior_credentials:
        try:
            os.remove(filename)
        except OSError, e:
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occured



