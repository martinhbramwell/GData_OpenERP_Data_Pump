#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell

The editor bug fix :   fromdos gDataTools.py  && sudo chown -R www-data:www-data /var/www/hasan/GData_OpenERP_Data_Pump

'''

import argparse
import creds
import gspread
import openerp_utils

from models.OErpModel import OErpModel

from peak.util.imports import lazyModule

connection = None

def dispatchTasks(wkbk, start_row):

    min_row = 0
    if start_row != None:  min_row = int(start_row) - 2

    shtTasks = wkbk.worksheet("Tasks")
    namesTasks = shtTasks.col_values(1)
    
    # Having the name of each handler, dispatch to them
    print 'Start work at spreadsheet row "{}" to Google.'.format(start_row)
    for row, task in enumerate(namesTasks):
        # print 'Row is #{}/{} '.format(row,min_row)
        if row > min_row:
            if task not in ("Model Class", "", None):
                print '\n\nTask#{} uses the module "{}".'.format(row + 1, task)
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    
                getattr(lazyModule('models.' + task), task)().process(wkbk, row)  

    return

def login(credentials):
    
    gc = {}
    
    # Get Google uid/pwd from ~/.gdataCreds  a file in the format
    #      {"user_id": "yourGoogleUID", "user_pwd": "yourGoogleUID"}

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
                
def getPumpCredentials(wkbk):

    shtCreds = wkbk.worksheet("Creds")
    lstlstCreds = shtCreds.get_all_values()
    
    creds = {t[0]:t[1] for t in lstlstCreds}

    return creds


def main():

    credentials = creds.get()
    google_connection = login(credentials)

    if google_connection is not None:
        if google_connection['connection'] is not None:

            OErpModel.gDataConnection = google_connection['connection']

            wkbk = OErpModel.gDataConnection.open_by_key(google_connection['workbook_key'])

            OErpModel.pumpCredentials = getPumpCredentials(wkbk)
            OErpModel.openErpConnection = openerp_utils.connect(OErpModel.pumpCredentials)
			
            dispatchTasks(wkbk, credentials['row'])

    print ''

if __name__ == '__main__':

    main()
	
