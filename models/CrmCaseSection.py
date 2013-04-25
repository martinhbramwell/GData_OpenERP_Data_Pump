#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'crm.case.section'

class CrmCaseSection(OErpModel):

    def __init__(self):
        super(CrmCaseSection, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'load': self.load
        }

    def process(self, wrksht, rowTask):
        super(CrmCaseSection, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(CrmCaseSection, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(CrmCaseSection, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(CrmCaseSection, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass


    def chkTask(self, parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(CrmCaseSection, self).load(parms, OPENERP_MODULE_NAME)
        print 'Done in CrmCaseSection!'


