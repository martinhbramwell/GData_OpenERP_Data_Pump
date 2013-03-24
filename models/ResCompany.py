#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.users'

class ResCompany(OErpModel):

    def process(self, wrksht, rowTask):
        super(ResCompany, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):
            print aMethod
            globals()[aMethod](self.parameters)
            pass


def chkTask(parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

