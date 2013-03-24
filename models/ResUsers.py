#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.users'

class ResUsers(OErpModel):

    def process(self, wrksht, rowTask):
        super(ResUsers, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):
            # print aMethod
            ### Temporary block            globals()[aMethod](self.parameters)
            pass


def chkTask(parms):
    print 'Task check for key "login" found : "' + parms['login'] + '"!'


def update(parms):
           
    user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)
    ids = user_model.search([("login", "=", "admin")])
    user_info = user_model.read(ids[0], ["name", "tz"])
    print user_info["name"] + " has timezone " + str(user_info["tz"])
    
    user_model.write(ids[0], {"tz":parms['tz']})

