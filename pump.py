#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

   The full program is explained here:
           http://martinhbramwell.github.io/GData_OpenERP_Data_Pump

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
        is the main entry point for running the GData_OpenERP_Data_Pump

'''

import sys
from persistence import drop_store

import gspread

# from utils import ConfigurationError
# import openerp_utils
import oerplib
import google_utils
import openerp_utils
import manage_arguments

from models.OErpModel import OErpModel

from peak.util.imports import lazyModule

connection = None


def dispatchTasks(wkbk, start_row):

    min_row = 0
    if start_row is None:
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
            if task not in ("Model Class", "", None)\
                    and int(stateTasks[row]) > 0:
                print '\n\nTask#{} uses the module "{}".'.format(row + 1, task)
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

                getattr(
                    lazyModule('models.' + task), task)().process(wkbk, row)
                complete += 1
    print 'Found {} tasks to process.'.format(complete)
    return


def main(workbook_key, start_row):

    print "Starting"
    google = google_utils.Google()

    if google is not None:

        OErpModel.gDataConnection = google.connect()

        print 'Workbook : {}'.format(workbook_key)
        wkbk = OErpModel.gDataConnection.open_by_key(workbook_key)

        creds = google_utils.getPumpCredentials(wkbk)
        OErpModel.pumpCredentials = creds

        if openerp_utils.OpenERP(creds) is not None:
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
