#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
import sys
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.users'
ignored_fields = ("ResUsers", "login")


class ResUsers(OErpModel):

    def __init__(self):
        super(ResUsers, self).__init__()

        self.methods = {
            'chkTask': self.chkTask, 'update': self.update, 'load': self.load
        }

    def process(self, wrksht, rowTask):
        super(ResUsers, self).process(wrksht, rowTask)

        pos = OErpModel.CONSTANTS['MAP_MASKS']

        # print '\n #   #   #   #   #   #   #   #   #   #  '

        for idx, aMethod in enumerate(self.methodNames):

            if super(ResUsers, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx + 1, aMethod)
                super(ResUsers, self).starting(idx)

                self.methods[aMethod](self.parameters)

                super(ResUsers, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx + 1, aMethod)

            # Temporary block            globals()[aMethod](self.parameters)
            pass

        # print ' #   #   #   #   #   #   #   #   #   #  \n'

    def update(self, parms):
        oerp = super(ResUsers, self).getConnection()

        # Obtain an array of record ids that match the selection criteria (only
        # one in this case)
        idUser = oerp.search(
            OPENERP_MODULE_NAME, [("login", "=", parms['login'])])[0]

        # Read the existing data (only what we need)
        aUser = oerp.browse(OPENERP_MODULE_NAME, idUser)
        print "Login " + parms['login'] + " -- " + aUser.login

        # Write it back out with update applied
        for key in parms:
            if key not in ignored_fields:    # Ignore the record key attribute
                val = OErpModel.parseSpecial(self, parms[key])
                print 'Editing : (User : {}, "{}":"{}") from "{}"'.format(
                    aUser.login, key, val, parms[key])
                setattr(aUser, key, val)

        oerp.write_record(aUser)
        print 'Written'

    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(ResUsers, self).load(parms, OPENERP_MODULE_NAME)
#        print 'Done in ResUsers!'

    def chkTask(self, parms):
        print 'Task check . . . '
        for key in parms:
            if key not in ("ResUsers", "login"):
                print "Key : " + key + "  Parm : "
                print OErpModel.parseSpecial(self, parms[key])
