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
            , 'show': self.show
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

        module_parms = super(ResPartnerBank, self).getWorkingSource(parms)

        # print 'Range : {}'.format(module_parms['data_range'])
        print module_parms

        print 'xxxx : '

        
        for col in module_parms['nameCol']:
            print 'Name : {}.  Number : {}.'.format(col, module_parms['nameCol'][col])

        print 'xxxx : '


    def show(self, parms):

        print '# - - prepare dictionary : destination data structure - - #'
        dataAcct = {
                          'id': ''
                        , 'bank_name': ''
                        , 'owner_name': ''
                        , 'bank_bic': ''
                        , 'zip': ''
                        , 'footer': ''
                        , 'sequence': 0
                        , 'country_id': ''
                        , 'company_id': ''
                        , 'journal_id': False
                        , 'currency_id': False
                        , 'state': ''
                        , 'street': ''
                        , 'state_id': ''
                        , 'partner_id': ''
                        , 'city': ''
                        , 'bank': ''
                        , 'acc_number': ''
                    }

        print '# - - prepare dictionary : source columns names to numbers - - #'

        titles = {}
        module_parms = super(ResPartnerBank, self).getWorkingSource(parms)
        print module_parms

        for col in module_parms['nameCol']:
            titles[col] = module_parms['nameCol'][col]
            print 'Name : {}.  Number : {}.'.format(col, titles[col])

        print '# - - prepare arrays : field names per data source  - - #'

        fieldNamesFromSpreadsheet = ['company_id', 'acc_number', 'bank_bic', 'state']

        fieldNamesFromResCompany = ['owner_name', 'acc_number', 'bank_bic', 'bank', 'state', 'bank_name']
        fieldNamesFromResBank = ['owner_name', 'acc_number', 'bank_bic', 'bank', 'state', 'bank_name']


        print '# - - prepare ids : database ids from external ids  - - #'

        rows = []
        numRow = module_parms['dictRange']['minRow']
        idx = 0
        while numRow <= module_parms['dictRange']['maxRow']:
            print 'Row #' + str(numRow)
            
            rows.append(module_parms['wksht'].row_values(numRow))
            print 'Bank code is ' + rows[idx][titles['bank_bic']-1]
            numRow += 1
            idx += 1



        '''
        print modelIrModelData.read(recIrModelData, ['res_id'])[0]['res_id']
        idPartner = modelIrModelData.search([("name", "=", "IridiumBlue"), ("model", "=", "res.company")])
        idBank = modelIrModelData.search([("name", "=", "BAAZ"), ("model", "=", "res.bank")])

        '''

        print '# - - prepare models - - #'

        modelResPartnerBank = self.openErpConnection.get_model(OPENERP_MODULE_NAME)

        modelIrModelData = self.openErpConnection.get_model("ir.model.data")
        modelResCompany = self.openErpConnection.get_model("res.company")
        modelResPartner = self.openErpConnection.get_model("res.partner")
        modelResBank = self.openErpConnection.get_model("res.bank")

        print 'Processing rows from spreadsheet.'

        idx = 0
        for row in rows:

            print '\n\nProcessing row#{}.'.format(idx)
            dataAcct = {}

            dataAcct['bank_bic'] = row[titles['bank_bic']-1]
            dataAcct['acc_number'] = row[titles['acc_number']-1]

            # dataAcct['state'] = super(ResPartnerBank, self).dbIdFromExtId(row[titles['state']-1], 'res.partner.bank.type', modelIrModelData)
            dataAcct['state'] = row[titles['state']-1]


            dataAcct['bank'] = super(ResPartnerBank, self).dbIdFromExtId(dataAcct['bank_bic'], 'res.bank', modelIrModelData)
            bank = modelResBank.read([dataAcct['bank']])[0]
            dataAcct['bank_name'] = bank['name']

            print 'Bank code of {} finds bank {} having id #{}.'.format(dataAcct['bank_bic'], bank['name'], dataAcct['bank'])


            
            cmpny = row[titles['company_id']-1]
            dataAcct['company_id'] = super(ResPartnerBank, self).dbIdFromExtId(cmpny, 'res.company', modelIrModelData)
            company = modelResCompany.read([dataAcct['company_id']])[0]

            dataAcct['partner_id'] = company['partner_id'][0]
            print '#######################  {}  #########################'.format( dataAcct['partner_id'])
            dataAcct['street'] = company['street'].encode('utf-8')
            dataAcct['owner_name'] = company['name'].encode('utf-8')
            dataAcct['city'] = company['city'].encode('utf-8')
            dataAcct['zip'] = company['zip']
            dataAcct['country_id'] = company['country_id'][0]
            dataAcct['state_id'] = company['state_id'][0]
            dataAcct['footer'] = False
            dataAcct['journal_id'] = False
            dataAcct['currency_id'] = False
            dataAcct['sequence'] = 0


            print 'Company code of {} finds company {} having id of {}.'.format(cmpny, company['name'], dataAcct['company_id'])
            
            dataAcct['id'] = dataAcct['bank_bic'] + dataAcct['acc_number']

            dataAcct['name'] = '/'

            for item, val in dataAcct.iteritems():
                print '{} = {}'.format(item, val)

            print 'Committing {}'.format(dataAcct['id'])

            modelResPartnerBank.create(dataAcct)

            print 'Processed row#{} --------------------'.format(idx)

            idx += 1

        return

        '''
        print 'state_id = {}'.format(user_model.read(thisCompany, ['state_id'])['state_id'][0])
        print 'country_id = {}'.format(user_model.read(thisCompany, ['country_id'])['country_id'][0])
        print 'partner_id = {}'.format(user_model.read(thisCompany, ['partner_id'])['partner_id'][0])
        print 'city = {}'.format(user_model.read(thisCompany, ['city'])['city'].encode('utf-8'))
        print 'zip = {}'.format(user_model.read(thisCompany, ['zip'])['zip'].encode('utf-8'))
        print 'name = {}'.format(user_model.read(thisCompany, ['name'])['name'])
        print 'bank_name = {}'.format(bank_model.read(thisBank, ["name"])["name"])
        print 'bank_bic = {}'.format(bank_model.read(thisBank, ["bic"])["bic"])
	
        '''

 






        modelResCompany = self.openErpConnection.get_model("res.company")
        thisCompany = modelResCompany.search([("name", "=", "IridiumBlue")])[0]
        dictCompanyFields = modelResCompany.fields_get()
        for aField in dictCompanyFields:
            print modelResCompany.read(thisCompany, [aField])
            print '  -  -  -  -  -  -  -  -  -  - '



        print user_model.read(thisCompany, ["partner_id"])

        bank_model = self.openErpConnection.get_model("res.bank")

        thisBank = bank_model.search([("bic", "=", codeBank)])[0]
        print 'Bank BMAC has id {}.'.format(bank_model.read(thisBank, ["id"])["id"])

        dictFields = user_model.fields_get()
        for aField in dictFields:
            print user_model.read(thisCompany, [aField])
            print '  -  -  -  -  -  -  -  -  -  - '

# -----

        print 'state_id = {}'.format(user_model.read(thisCompany, ['state_id'])['state_id'][0])
        print 'country_id = {}'.format(user_model.read(thisCompany, ['country_id'])['country_id'][0])
        print 'partner_id = {}'.format(user_model.read(thisCompany, ['partner_id'])['partner_id'][0])
        print 'city = {}'.format(user_model.read(thisCompany, ['city'])['city'].encode('utf-8'))
        print 'zip = {}'.format(user_model.read(thisCompany, ['zip'])['zip'].encode('utf-8'))
        print 'name = {}'.format(user_model.read(thisCompany, ['name'])['name'])
        print 'bank_name = {}'.format(bank_model.read(thisBank, ["name"])["name"])
        print 'bank_bic = {}'.format(bank_model.read(thisBank, ["bic"])["bic"])

 
        '''
	
        '''

        dataAcct = {
                          'id': codeBank + numAcct
                        , 'bank_name': bank_model.read(thisBank, ["name"])["name"]
                        , 'bank_bic': bank_model.read(thisBank, ["bic"])["bic"]
                        , 'zip': ''
                        , 'footer': False
                        , 'owner_name': 'Iridium Blue'
                        , 'sequence': 321
                        , 'journal_id': False
                        , 'currency_id': False
                        , 'country_id': user_model.read(thisCompany, ['country_id'])['country_id'][0]
                        , 'company_id': user_model.read(thisCompany, ['id'])['id']
                        , 'state': typeAcct
                        , 'street': user_model.read(thisCompany, ['street'])['street'].encode('utf-8')
                        , 'state_id': user_model.read(thisCompany, ['state_id'])['state_id'][0]
                        , 'partner_id': user_model.read(thisCompany, ['partner_id'])['partner_id'][0]
                        , 'city': user_model.read(thisCompany, ['city'])['city'].encode('utf-8')
                        , 'bank': bank_model.read(thisBank, ["id"])["id"]
                        , 'acc_number': numAcct
                    }

        user_model = self.openErpConnection.get_model(OPENERP_MODULE_NAME)
        print user_model.create(dataAcct)


        print 'Listing attributes of {}.'.format(OPENERP_MODULE_NAME)


        '''
        thisAcct = user_model.search([("acc_number", "=", "3232323232")])[0]

        dictFields = user_model.fields_get()
        for aField in dictFields:
            print user_model.read(thisAcct, [aField])
        '''




        print 'Done in ResPartnerBank!'



    def load(self, parms):
        print 'Calling parent to load to "{}".'.format(OPENERP_MODULE_NAME)

        data = super(ResPartnerBank, self).load(parms, OPENERP_MODULE_NAME)
        print 'Done in ResPartnerBank!'
'''
thisAcct = user_model.search([("name", "=", parms['login'])])[0]
dictData = user_model.read()


'''
