#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.company'

class ResCompany(OErpModel):

    def __init__(self):
        super(ResCompany, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'load': self.load
        }


    def process(self, wrksht, rowTask):
        super(ResCompany, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(ResCompany, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(ResCompany, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(ResCompany, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass


    def chkTask(self, parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'


    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(ResCompany, self).load(parms, OPENERP_MODULE_NAME)
        print 'Done in ResCompany!'
