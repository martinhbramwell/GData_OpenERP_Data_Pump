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
        print 'Task check . . . '
        for key  in parms:
            if key not in ("ResUsers", "login"):
                print "Key : " + key + "  Parm : "
                print OErpModel.parseSpecial(self, parms[key])
    
    
    def update(self, parms):
               
        user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)

        thisUser = user_model.search([("login", "=", parms['login'])])[0]
        nameUser = user_model.read(thisUser, ["name"])["name"]
        print "Login " + parms['login'] + " -- " + nameUser

        user_info = user_model.read(thisUser, ["in_group_4", "in_group_6", "tz", "active"])

        for key  in parms:
            if key not in ("ResUsers", "login"):  
                val = OErpModel.parseSpecial(self, parms[key]) 
                print 'Writing : (thisUser, "{}":"{}") from "{}"'.format(key, val, parms[key])
                user_model.write(thisUser, {key:val})

