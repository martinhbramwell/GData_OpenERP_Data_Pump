#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''
from OErpModel import OErpModel

OPENERP_MODULE_NAME = 'ir.property'

class IrProperty(OErpModel):

    def __init__(self):
        super(IrProperty, self).__init__()
        
        self.methods = {
              'chkTask': self.chkTask, 'map': self.map
        }


    def process(self, wrksht, rowTask):
        super(IrProperty, self).process(wrksht, rowTask)
        
        for idx, aMethod in enumerate(self.methodNames):

            if super(IrProperty, self).todo(idx):
                print '    #{} Doing "{}" now.'.format(idx+1, aMethod)
                super(IrProperty, self).starting(idx)


            	self.methods[aMethod](self.parameters)


                super(IrProperty, self).finished(idx)
                print '__'
            else:
                print '    #{} Skipping "{}"!'.format(idx+1, aMethod)

            pass

    def map(self, parms):

        oerp = super(IrProperty, self).getConnection()
        
        module_parms = super(IrProperty, self).getWorkingSource(parms)
        wksht = module_parms['wksht']
        numCols = module_parms['numCols']
        nameCol = module_parms['nameCol']
        
        print " wkbk -- {}".format(module_parms['wkbk'])
        print " wksht -- {}".format(wksht)
        print " dictRange -- {}".format(module_parms['dictRange'])
        print " numCols -- {}".format(numCols)
        print " nameCol -- {}".format(module_parms['nameCol'])

        fields = wksht.row_values(int(parms['titles_row']))[:numCols:]
        print ' - - - fields - - - '
        print fields
        
        rng =  wksht.range(parms['data_range'])
        data = self.groupToArray(numCols, [cell.value for cell in rng])
        print ' - - -  data  - - - '
        properties = []
        for row in data:
            print str(row)[:160]
            company = row[nameCol['company_id'] - 1]
            map_type = row[nameCol['map_type'] - 1]
            target_uid = row[nameCol['target_uid'] - 1]
            target_model = row[nameCol['target_model'] - 1]
            source_model = row[nameCol['source_model'] - 1]
            source_field = row[nameCol['source_field'] - 1]
            
            aMap = OErpModel.get_mapping_by_property(self, source_model, source_field)

            fields_id = "{}.{}".format(aMap['module'], aMap['name'])
            print fields_id
            
            obj_id = OErpModel.get_object_id_by_code(self, target_model, target_uid)
            value_reference = "{}.{}".format(target_model, obj_id)
            print "value_reference = {}".format(value_reference)
            
            prprty = [source_field, map_type, fields_id, company, value_reference]
            print prprty
            properties.append(prprty)

        titles = ['name', 'type', 'fields_id/id', 'company_id/id', 'value_reference']
        oerpModel = oerp.get(OPENERP_MODULE_NAME)
        oerpModel.load(titles, properties)

        '''
        INSERT INTO "ir_property" (
                                 "id",     "value_reference", "type"    , "name"                       , "create_uid", "write_uid", "create_date"             ,              "write_date") VALUES(
        nextval('ir_property_id_seq'), 'account.account.237', 'many2one', 'property_account_receivable',            1,           1, (now() at time zone 'UTC'), (now() at time zone 'UTC'))
        '''


    def chkTask(self, parms):
        print 'Check for "docs_key" found : "' + parms['docs_key'] + '"!'
        print 'Check for "docs_sheet" found : "' + parms['docs_sheet'] + '"!'

