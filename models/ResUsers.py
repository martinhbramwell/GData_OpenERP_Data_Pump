#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.users'

class ResUsers(OErpModel):

    def __init__(self):
        super(ResUsers, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'update': self.update
        }

    def process(self, wrksht, rowTask):
        super(ResUsers, self).process(wrksht, rowTask)

        pos  = OErpModel.CONSTANTS['MAP_MASKS']

        # print '\n #   #   #   #   #   #   #   #   #   #  '
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(ResUsers, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(ResUsers, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(ResUsers, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)


            ### Temporary block            globals()[aMethod](self.parameters)
            pass

        # print ' #   #   #   #   #   #   #   #   #   #  \n'

    def chkTask(self, parms):
        print 'Task check for key "login" found : "' + parms['login'] + '"!'
    
    
    def update(self, parms):
               
        user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)
        ids = user_model.search([("login", "=", "admin")])
        user_info = user_model.read(ids[0], ["name", "tz"])
        print user_info["name"] + " has timezone " + str(user_info["tz"])
        
        user_model.write(ids[0], {"tz":parms['tz']})

