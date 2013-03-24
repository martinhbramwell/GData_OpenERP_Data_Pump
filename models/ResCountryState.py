#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.country.state'

class ResCountryState(OErpModel):

    def __init__(self):
        super(ResCountryState, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'load': self.load
        }

    def process(self, wrksht, rowTask):
        super(ResCountryState, self).process(wrksht, rowTask)
        
        THIS_MODULE_NAME = self.moduleName
        
        print self.methodNames
        
        for idx, aMethod in enumerate(self.methodNames):
            self.methods[aMethod](self.parameters)

    def chkTask(self, parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

    def load(self, parms):
        print 'Loading to "{}".'.format(OPENERP_MODULE_NAME)
        wkbk = OErpModel.gDataConnection.open_by_key(parms['docs_key'])
        wksht = wkbk.worksheet(parms['docs_sheet'])
        
        dictRange = super(ResCountryState, self).getCellsRange(wksht, parms['range'])
                
        fields = wksht.row_values(int(parms['titles_row']))
        print ' - - - fields - - - '
        print fields
        
        data = super(ResCountryState, self).groupToArray(3, [cell.value for cell in wksht.range(parms['range'])])
        print ' - - -  data  - - - '
        for idx in range(4):
            print data[idx]

        user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)
        user_model.load(fields, data)
        print 'Done!'
        

