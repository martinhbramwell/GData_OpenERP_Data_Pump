#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'ir.module.module'

class IrModuleModule(OErpModel):

    def __init__(self):
        super(IrModuleModule, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'install_update_module': self.install_update_module
        }

    def process(self, wrksht, rowTask):
        super(IrModuleModule, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(IrModuleModule, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(IrModuleModule, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(IrModuleModule, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)


            ### Temporary block            globals()[aMethod](self.parameters)
            pass


    def chkTask(self, parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

    def install_update_module(self, parms):
        # install/update/upgrade module
        print " - * - * - * - * - * - * - * - * - * - *"
        nameModule = connection.get_model(OPENERP_MODULE_NAME)
        print "nameModule " + nameModule
        idModule = nameModule.search([('name', '=', parms['name'])])
        print "idModule " + idModule
        module = nameModule.read(idModule[0])
        print '{0}'.format(module['state'])
        if not module['state'] == 'installed':
            print 'installing "{0}"'.format(name)
            nameModule.button_immediate_install([idModule[0]])
        elif update:
            print 'upgrading "{0}"'.format(name)
            nameModule.button_upgrade([idModule[0]])
            upgrade_id = connection.get_model('base.module.upgrade').create({'module_info': idModule[0]})
            connection.get_model('base.module.upgrade').upgrade_module(upgrade_id)
        else:
            print 'skipping "{0}"'.format(name) 



