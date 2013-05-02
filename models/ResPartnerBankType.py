#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.partner.bank.type'

class ResPartnerBankType(OErpModel):

    def __init__(self):
        super(ResPartnerBankType, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'load': self.load
            , 'show': self.show
        }


    def process(self, wrksht, rowTask):
        super(ResPartnerBankType, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(ResPartnerBankType, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(ResPartnerBankType, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(ResPartnerBankType, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass


    def chkTask(self, parms):
        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'


    def show(self, parms):
        print 'Listing attributes of {}.'.format(OPENERP_MODULE_NAME)
        user_model = self.openErpConnection.get_model(OPENERP_MODULE_NAME)
        dictFields = user_model.fields_get()
        for aField in dictFields:
            print 'Field : {}.'.format(aField)


        print 'Done in ResPartnerBankType!'


    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(ResPartnerBankType, self).load(parms, OPENERP_MODULE_NAME)
        print 'Done in ResPartnerBankType!'
