#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel
import openerplib

OPENERP_SERVICE_NAME = 'db'

class Database(OErpModel):

    def __init__(self):
        super(Database, self).__init__()
        
        self.methods = {
                'chkTask': self.chkTask
              , 'create': self.create
        }


    def process(self, wrksht, rowTask):
        super(Database, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(Database, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(Database, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(Database, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass

    def create(self, parms):

        #  Handle db creation

        port = int(OErpModel.pumpCredentials['host_port'])
        db = OErpModel.pumpCredentials['db_name']
        host = OErpModel.pumpCredentials['host_name']
        user = OErpModel.pumpCredentials['user_id']
        pwd = OErpModel.pumpCredentials['user_pwd']
        context = OErpModel.pumpCredentials['user_context']
        pwdSuper = OErpModel.pumpCredentials['super_pwd']

        print 'Obtaining service : {} on host {}:{}'.format(OPENERP_SERVICE_NAME, host, port)
        db_service=openerplib.get_connector(host, 'xmlrpc', port).get_service(OPENERP_SERVICE_NAME)
        print 'Services : {0}'.format(db_service.list())
        if not db_service.db_exist(db):
            # none threading as we rely on the db further on
            print 'Will create database "{}" now; with user pwd "{}", master pwd "{}" and context "{}"'.format(db, pwd, pwdSuper, context)
            db_service.create_database(pwdSuper, db, False, context, pwd)
        else:
            print 'Using existing database "{0}"'.format(db) 


    def chkTask(self, parms):
        print 'Task check for key "first_parm" found : "' + parms['first_parm'] + '"!'
        print OErpModel.pumpCredentials['host_port']
        print OErpModel.pumpCredentials['db_name']
        print OErpModel.pumpCredentials['host_name']

