#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
import sys
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'ir.mail_server'
identifier = "name"
ignored_fields = ("IrMailServer", identifier)


class IrMailServer(OErpModel):

    def __init__(self):
        super(IrMailServer, self).__init__()

        self.methods = {
            'chkTask': self.chkTask, 'update': self.update, 'load': self.load
        }

    def process(self, wrksht, rowTask):
        super(IrMailServer, self).process(wrksht, rowTask)

        pos = OErpModel.CONSTANTS['MAP_MASKS']

        # print '\n #   #   #   #   #   #   #   #   #   #  '

        for idx, aMethod in enumerate(self.methodNames):

            if super(IrMailServer, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx + 1, aMethod)
                super(IrMailServer, self).starting(idx)

                self.methods[aMethod](self.parameters)

                super(IrMailServer, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx + 1, aMethod)

            # Temporary block            globals()[aMethod](self.parameters)
            pass

        # print ' #   #   #   #   #   #   #   #   #   #  \n'

    def update(self, parms):
        oerp = super(IrMailServer, self).getConnection()

        # Read the existing data (only what we need)
        idMailServer = oerp.search(
            OPENERP_MODULE_NAME, [(identifier, 'ilike', parms[identifier])])[0]
        theMailServer = oerp.browse(OPENERP_MODULE_NAME, idMailServer)
        print "Mail server named {}".format(theMailServer.name)

        # Write it back out with update applied
        for key in parms:
            if key not in ignored_fields:    # Ignore the record key attribute
                val = OErpModel.parseSpecial(self, parms[key])
                print 'Editing : (Mail server : {}, "{}":"{}") from "{}"'.format(
                    parms[identifier], key, val, parms[key])
                setattr(theMailServer, key, val)

        oerp.write_record(theMailServer)
        print 'Written'

    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(IrMailServer, self).load(parms, OPENERP_MODULE_NAME)
#        print 'Done in IrMailServer!'

    def chkTask(self, parms):
        print 'Task check . . . '
        for key in parms:
            if key not in ("IrMailServer", "login"):
                print "Key : " + key + "  Parm : "
                print OErpModel.parseSpecial(self, parms[key])
