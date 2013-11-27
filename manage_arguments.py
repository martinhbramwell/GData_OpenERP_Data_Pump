#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''

import argparse
PROG = "gDataTools.py"

def get():

    desc = 'A very simple tool for feeding Google Spreadsheet data into the XMLRPC channel of OpenERP V7. Please read about it here:\n'
    desc += 'https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/blob/master/README.md'
    
    usage = "usage: {} [options] arg".format(PROG)
    parser = argparse.ArgumentParser(description=desc, prog = PROG)
    
    # Required
    choose = parser.add_mutually_exclusive_group(required=True)
    choose.add_argument("-c", "--clean", action='store_true', help = "to drop and create new credentials")
    choose.add_argument('-k', '--workbook_key', help = 'The identity key of a Google Spreadsheets workbook.')

    # Optional
    parser.add_argument("-r", "--start_row", default = 4, dest="start_row"
                      , help = "Row in Tasks sheet at which to start processing.")
    
    return parser.parse_args()
    
if __name__ == '__main__':
    
    args = get()
    
    print args.clean
    print args.workbook_key
    print args.start_row


