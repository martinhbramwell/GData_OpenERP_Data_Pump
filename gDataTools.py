#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''

   The full program is explained here:  http://martinhbramwell.github.io/GData_OpenERP_Data_Pump

    Copyright (C) 2013 warehouseman.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Created on 2013-03-19

    @author: Martin H. Bramwell

    This module:
       This module is the main entry point for running the GData_OpenERP_Data_Pump

'''

import sys
from persistence import drop_store


# FIXME - - 
#import argparse
#import creds
# - - - 

import gspread

# from utils import ConfigurationError
import openerp_utils
import google_utils
import manage_arguments

from models.OErpModel import OErpModel

from peak.util.imports import lazyModule

connection = None

def dispatchTasks(wkbk, start_row):

    min_row = 0
    if start_row == None:
        min_row = 2
    else:
        min_row = int(start_row) - 2

    shtTasks = wkbk.worksheet("Tasks")
    namesTasks = shtTasks.col_values(1)
    stateTasks = shtTasks.col_values(4)
    
    # Having the name of each handler, dispatch to them
    print 'Start work at row #{} in the "Tasks" sheet.'.format(min_row + 2)
    complete = 0
    for row, task in enumerate(namesTasks):
        # print 'Row is #{}/{} '.format(row,min_row)
        # print 'Task #{} has {} to do.'.format(row+1,stateTasks[row])
        if row > min_row:
            if task not in ("Model Class", "", None) and int(stateTasks[row]) > 0:
                    print '\n\nTask#{} uses the module "{}".'.format(row + 1, task)
                    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        
                    getattr(lazyModule('models.' + task), task)().process(wkbk, row)
                    complete += 1
    print 'Found {} tasks to process.'.format(complete)
    return


'''
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
'''
                
def getPumpCredentials(wkbk):

    shtCreds = wkbk.worksheet("Creds")
    lstlstCreds = shtCreds.get_all_values()
    
    creds = {t[0]:t[1] for t in lstlstCreds}

    return creds

def main(workbook_key, start_row):

    print "Starting"
    google_connection = google_utils.GoogleConnection()
        
    if 1 == 0:
        gc = google_connection.connection
        
        #
        wkbk = gc.open_by_url(spreadsheet_url)
        cnt = 1
        print 'Found sheets:'
        for sheet in wkbk.worksheets():
            print ' - Sheet #{}: Id = {}  Title = {}'.format(cnt, sheet.id, sheet.title)
            cnt += 1
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        print "Done"
        exit(-1)
    

    if google_connection is not None:
        if google_connection.connection is not None:

            OErpModel.gDataConnection = google_connection.connection

            print 'Workbook : {}'.format(workbook_key)
            wkbk = OErpModel.gDataConnection.open_by_key(workbook_key)

            OErpModel.pumpCredentials = getPumpCredentials(wkbk)
            OErpModel.openErpConnection = openerp_utils.connect(OErpModel.pumpCredentials)
			
            dispatchTasks(wkbk, start_row)

    print ''

if __name__ == '__main__':
    
    args = manage_arguments.get()
    
    print args.clean
    print args.workbook_key
    print args.start_row    
    
    if args.clean:
        drop_store()
        print "Store dropped."
        exit(0)
        
    main(args.workbook_key, args.start_row)
    exit(0)

