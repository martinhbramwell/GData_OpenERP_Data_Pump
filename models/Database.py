#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel
from openerp_utils import db_connect

import oerplib

OPENERP_SERVICE_NAME = 'db'


class Database(OErpModel):

    def __init__(self):
        super(Database, self).__init__()

        self.methods = {
            'chkTask': self.chkTask, 'create': self.create
        }

    def process(self, wrksht, rowTask):
        super(Database, self).process(wrksht, rowTask)

        for idx, aMethod in enumerate(self.methodNames):

            if super(Database, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx + 1, aMethod)
                super(Database, self).starting(idx)

                self.methods[aMethod](self.parameters)

                super(Database, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx + 1, aMethod)

            pass

    def create(self, parms):

        #  Handle db creation

        server = OErpModel.openErpConnection['super']
        if server is not None:
            db = OErpModel.pumpCredentials['db_name']
            if db in server.db.list():
                print 'Using existing database "{0}"'.format(db)
            else:
                user = OErpModel.pumpCredentials['user_id']
                pwd = OErpModel.pumpCredentials['user_pwd']
                context = OErpModel.pumpCredentials['user_context']
                pwdSuper = OErpModel.pumpCredentials['super_pwd']

                msg = 'Will create database "{}" now; with'.format(db)
                msg += ' user pwd "{}", context "{}"'.format(pwd, context)
                print msg

                server.db.create_and_wait(pwdSuper, db, False, context, pwd)
                db_connect(user, pwd, db)
        else:
            print 'Using existing database "{0}"'.format(db)

    def chkTask(self, parms):
        print "Check for 'first_parm' found : {}!".format(parms['first_parm'])

        print OErpModel.pumpCredentials['host_port']
        print OErpModel.pumpCredentials['db_name']
        print OErpModel.pumpCredentials['host_name']
