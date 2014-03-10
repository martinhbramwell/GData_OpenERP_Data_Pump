#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'crm.lead'


class CrmLead(OErpModel):

    def __init__(self):
        super(CrmLead, self).__init__()

        self.methods = {
            'chkTask': self.chkTask, 'load': self.load
        }

    def process(self, wrksht, rowTask):
        super(CrmLead, self).process(wrksht, rowTask)

        for idx, aMethod in enumerate(self.methodNames):

            if super(CrmLead, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx + 1, aMethod)
                super(CrmLead, self).starting(idx)

                self.methods[aMethod](self.parameters)

                super(CrmLead, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx + 1, aMethod)

            pass

    def chkTask(self, parms):
        print 'Check for "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Check for "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(CrmLead, self).load(parms, OPENERP_MODULE_NAME)
        print 'Done in CrmLead!'
