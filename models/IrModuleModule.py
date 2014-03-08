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
            , 'install_module': self.install_module
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
        print 'Task check for key "titles_row" found : "' + parms['titles_row'] + '"!'
        print 'Task check for key "data_range" found : "' + parms['data_range'] + '"!'


    def install_module(self, parms):
        oerp = super(IrModuleModule, self).getConnection()

        print " - * - * - * - * - * - * - * - * - * - *"
        oerp.config['timeout'] = 4 * oerp.config['timeout']

        oerpModel = oerp.get(OPENERP_MODULE_NAME)

        module_parms = super(IrModuleModule, self).getWorkingSource(parms)
        listModuleNames = module_parms['wksht'].col_values(1)

        idx = module_parms['dictRange']['minRow'] - 1
        while (idx < module_parms['dictRange']['maxRow']):
            nameModule = listModuleNames[idx]
            print 'Module name : ' + nameModule
            idModule = oerpModel.search([('name', '=', nameModule)])[0]
            print "Module ID #" + str(idModule)
            module = oerpModel.read(idModule)
            stateModule = module['state']

            if not module['state'] == 'installed':
                print 'Now installing module "{}"'.format(nameModule)
                oerpModel.button_immediate_install([idModule])
            else:
                print 'Doing nothing with module "{}" in state "{}"'.format(nameModule, stateModule) 

            idx += 1

        oerp.config['timeout'] = oerp.config['timeout'] / 4

