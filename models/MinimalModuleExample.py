#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = '  - - - MINIMALMODULEEXAMPLE - - - '

class MinimalModuleExample(OErpModel):

    def __init__(self):
        super(MinimalModuleExample, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
        }


    def process(self, wrksht, rowTask):
        super(MinimalModuleExample, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(MinimalModuleExample, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(MinimalModuleExample, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(MinimalModuleExample, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass



    def chkTask(self, parms):
        print 'Task check for key "first_parm" found : "' + parms['first_parm'] + '"!'

