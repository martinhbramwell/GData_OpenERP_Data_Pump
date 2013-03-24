#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.users'

class MinimalModuleExample(OErpModel):

    def process(self, wrksht, rowTask):
        super(MinimalModuleExample, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):
            print aMethod
            globals()[aMethod](self.parameters)
            pass


def chkTask(parms):
    print 'Task check for key "first_parm" found : "' + parms['first_parm'] + '"!'

