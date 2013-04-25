#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'base.language.install'

class BaseLanguageInstall(OErpModel):

    def __init__(self):
        super(BaseLanguageInstall, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'install': self.install
        }

    def process(self, wrksht, rowTask):
        super(BaseLanguageInstall, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(BaseLanguageInstall, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(BaseLanguageInstall, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(BaseLanguageInstall, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass


    def chkTask(self, parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

    def install(self, parms):

        module_parms = super(BaseLanguageInstall, self).getWorkingSource(parms)
        languages = module_parms['wksht'].col_values(1)

        oerpModel = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)

        idx = module_parms['dictRange']['minRow'] - 1
        while (idx < module_parms['dictRange']['maxRow']):
            language = languages[idx]
            print 'Creating model for "{}" with "{}".'.format(language, OPENERP_MODULE_NAME)
            lid = oerpModel.create({'lang' : language})
            #lang_obj = oerpModel.read(lid)
            print 'Installing : ' + language
            oerpModel.lang_install([lid])
            print 'Installed : ' + language
            idx += 1


        '''
        languages = ['el_GR']
        for lang in languages:
        pass
    

        print 'Calling parent to install "{}".'.format(parms['lang'])

        # data = super(BaseLanguageInstall, self).load(parms, OPENERP_MODULE_NAME)
        print 'Done in BaseLanguageInstall!'

        '''
