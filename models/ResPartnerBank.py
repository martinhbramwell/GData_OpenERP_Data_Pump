#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'res.partner.bank'

class ResPartnerBank(OErpModel):

    def __init__(self):
        super(ResPartnerBank, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask
            , 'load': self.load
        }


    def process(self, wrksht, rowTask):
        super(ResPartnerBank, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(ResPartnerBank, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(ResPartnerBank, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(ResPartnerBank, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass


    def chkTask(self, parms):

        print 'Task check for key "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Task check for key "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

        return



    def load(self, parms):

        print 'Loading to "{}".'.format(OPENERP_MODULE_NAME)

        print '# - - prepare models - - #'
        modelResPartnerBank = self.openErpConnection.get_model(OPENERP_MODULE_NAME)


        print '# - - prepare dictionary : source columns names to numbers - - #'
        module_parms = super(ResPartnerBank, self).getWorkingSource(parms)
        titles = module_parms['nameCol']


        print '# - - prepare ids : database ids from external ids  - - #'

        numRow = module_parms['dictRange']['minRow']
        idx = 0
        while numRow <= module_parms['dictRange']['maxRow']:

            row = module_parms['wksht'].row_values(numRow)

            dataAcct = {}

            # Spreadsheet fields
            dataAcct['acc_number']  = row[titles['acc_number']-1]
            dataAcct['state']       = row[titles['state']-1]

            #  Company fields
            company = super(ResPartnerBank, self).getRecord("ResCompany", row[titles['company_id']-1], True)

            dataAcct['company_id']  = company['id']
            dataAcct['partner_id']  = company['partner_id'][0]
            dataAcct['street']      = company['street'].encode('utf-8')
            dataAcct['owner_name']  = company['name'].encode('utf-8')
            dataAcct['city']        = company['city'].encode('utf-8')
            dataAcct['zip']         = company['zip']
            dataAcct['country_id']  = company['country_id'][0]
            dataAcct['state_id']    = company['state_id'][0]


            #  Bank fields
            bank = super(ResPartnerBank, self).getRecord("ResBank", row[titles['bank_bic']-1], True)

            dataAcct['bank']        = bank['id']
            dataAcct['bank_name']   = bank['name']
            dataAcct['bank_bic']    = bank['name']

            dataAcct['id']          = dataAcct['bank_bic'] + dataAcct['acc_number']

            # Unused fields
            dataAcct['footer']      = False
            dataAcct['journal_id']  = False
            dataAcct['currency_id'] = False
            dataAcct['sequence']    = 0
            dataAcct['name']        = '/'
            
            # Create the new record
            modelResPartnerBank.create(dataAcct)

            print 'Processed row#{} '.format(idx)

            idx += 1
            numRow += 1


        print 'Done in ResPartnerBank!'

        return

