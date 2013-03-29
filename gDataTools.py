#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''

import argparse
import creds
import gspread
import openerp_utils

from models.OErpModel import OErpModel

from peak.util.imports import lazyModule

connection = None

def dispatchTasks(wkbk):

    shtTasks = wkbk.worksheet("Tasks")
    namesTasks = shtTasks.col_values(1)
    
    # Having the name of each handler, dispatch to them
    for row, task in enumerate(namesTasks):
        if row > 1:
            print '\n\nTask#{} uses the module "{}".'.format(row - 1, task)
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

            getattr(lazyModule('models.' + task), task)().process(wkbk, row)  
    return

def login():
    
    gc = {}
    
    # Get Google uid/pwd from ~/.gdataCreds  a file in the format
    #      {"user_id": "yourGoogleUID", "user_pwd": "yourGoogleUID"}
    credentials = creds.get()

    gc['workbook_key'] = credentials['key']
    
    if credentials['user_pwd'] is not None:
        if credentials['user_id'] is not None: 
            try:
                gc['connection'] = gspread.login(credentials['user_id'], credentials['user_pwd'])
                print 'Connected user "{}" to Google.'.format( credentials['user_id'])
                return gc
            except gspread.exceptions.AuthenticationError, e:
                print "Google rejected those credentials."
                creds.silentremove(creds.credential_path)
                return None
        
        else:
            print 'Google connection : ', 'No user id was supplied.  Use --u or --uid'
    else:
        print 'Google connection : ', 'No user password was supplied.  Use -p or --pwd'
        
    creds.silentremove(creds.credential_path)
    return None
                


def main():

    google_connection = login()
    if google_connection is not None:
        if google_connection['connection'] is not None:
			
            wkbk = google_connection['connection'].open_by_key(google_connection['workbook_key'])
            OErpModel.gDataConnection = google_connection['connection']
			
            OErpModel.openErpConnection = openerp_utils.connect(wkbk)
            dispatchTasks(wkbk)

    print ''

if __name__ == '__main__':

    main()
	

