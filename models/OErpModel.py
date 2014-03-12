#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''

import sys
from peak.util.imports import lazyModule

import oerplib

class UnkownRecordError(Exception):
    pass

external_id_mapper = 'ir.model.data'

class OErpModel(object):

    openErpConnection = {'super': None, 'admin': None}
    gDataConnection = None
    pumpCredentials = None
    
    CONSTANTS = {}
    
    CONSTANTS['COMPLETION_MAP'] = 2
    CONSTANTS['INCOMPLETION_MAP'] = CONSTANTS['COMPLETION_MAP'] + 1
    CONSTANTS['MAP_MASK'] = CONSTANTS['INCOMPLETION_MAP'] + 1
    
    CONSTANTS['FIRST_ACTION_STEP'] = CONSTANTS['MAP_MASK'] + 1
    CONSTANTS['LAST_ACTION_STEP'] = 8 + CONSTANTS['FIRST_ACTION_STEP'] - 1
    
    CONSTANTS['END_OF_LINE'] = 'EOL'
    
    CONSTANTS['MAP_MASKS'] = [
                  0b00000001
                , 0b00000010
                , 0b00000100
                , 0b00001000
                , 0b00010000
                , 0b00100000
                , 0b01000000
                , 0b10000000
                ]

    def __init__(self):
    
        self.parameters = {}
        self.module_parms = []
        self.task_parms = []
        
        self.methodNames = []
        self.moduleName = ''

        self.done = -1
        self.todo = -1
        self.mask = -1

        self.shtTasks = None
        self.currentRow = -1

        self.modelIrModelData = None

    def getConnection(self):
        if OErpModel.openErpConnection['admin'] is None:
            sys.exit("You are not logged in to '{}' as user {}.".format(self.pumpCredentials['db_name'], self.pumpCredentials['user_id']))
        return OErpModel.openErpConnection['super']

    def setIrModelDataModel(self):
        self.modelIrModelData = self.openErpConnection.get_model("ir.model.data")


    def getRecord(self, model, id, external=False):
        if self.modelIrModelData == None:
            self.setIrModelDataModel()

        return getattr(lazyModule('models.' + model), model)().getRecord(id, external)

    def starting(self, idx):
        # print 'Starting #' + str(idx)

        bit = ((self.mask -1) << idx) & self.mask
        col = 1 + OErpModel.CONSTANTS['INCOMPLETION_MAP']
        row = self.currentRow + 1

        incomplete = int(self.shtTasks.cell(row, col).value)    # cell(row, col)
        self.shtTasks.update_cell(row, col, bit & incomplete)   # update_cell(row, col, value)
        # print 'Cleared bit #' + str(bit) + '(with ' + str(bit & incomplete) + ') in column #' + str(col) + ' and row #' + str(row)

    def finished(self, idx):
        # print 'Finished #' + str(idx)

        bit = 1 << idx
        col = 1 + OErpModel.CONSTANTS['COMPLETION_MAP']
        row = self.currentRow + 1

        incomplete = int(self.shtTasks.cell(row, col).value)    # cell(row, col)
        self.shtTasks.update_cell(row, col, bit | incomplete)   # update_cell(row, col, value)

        # print 'Set the bit #' + str(bit) + '(with ' + str(bit | incomplete) + ') in column #' + str(col) + ' and row #' + str(row)

        

        
    def process(self, wrksht, rowTask):
    
        print 'Processing row #{} from "Task" sheet'.format(rowTask + 1)
        self.currentRow = rowTask
        
        self.shtTasks = wrksht.worksheet("Tasks")
        shtParms = wrksht.worksheet("Parms")

        self.task_parms = self.shtTasks.row_values(rowTask+1)
        print 'Task parameters found in range "{}".'.format(self.task_parms[1])
        
        parms_cells = shtParms.range(self.task_parms[1])
        
        self.module_parms = [cell.value for cell in parms_cells]
        self.moduleName = self.module_parms[0]
        
        max = len(self.module_parms) / 2
        for col in range(max):
            self.parameters[self.module_parms[col]] = self.module_parms[col + max]
            
        for idx, parm in enumerate(self.task_parms):
            # print str(idx) + ' : ' + str(OErpModel.CONSTANTS['FIRST_ACTION_STEP']) + ' - ' + parm

            if idx == OErpModel.CONSTANTS['COMPLETION_MAP'] :   self.done = int(parm)
            if idx == OErpModel.CONSTANTS['INCOMPLETION_MAP'] : self.todo = int(parm)
            if idx == OErpModel.CONSTANTS['MAP_MASK'] :         self.mask = int(parm)
            if     parm != OErpModel.CONSTANTS['END_OF_LINE'] \
                and idx <= OErpModel.CONSTANTS['LAST_ACTION_STEP'] \
                and idx >= OErpModel.CONSTANTS['FIRST_ACTION_STEP']:
                self.methodNames.append(parm)                



    def todo(self, idx):
        # print 'should we do #' + str(idx)   + '?    ?    ?    ?    ?    ?    ?    ?    ?    ?    ?    ?    ?    '
        # print 'Pos mask : ' + str(OErpModel.CONSTANTS['MAP_MASKS'][idx])
        # print 'Done     : ' + str(self.done)
        # print 'ToDo     : ' + str(self.todo)
        # print 'ToDo Mask: ' + str(self.mask)
        # print ' . . . . . . . . . . . . . . . . . . '

        maskedToDo = (self.todo & self.mask & OErpModel.CONSTANTS['MAP_MASKS'][idx]) >> idx
        maskedDone = (~self.done & self.mask & OErpModel.CONSTANTS['MAP_MASKS'][idx]) >> idx

        # print 'Masked To Do : ' + str(maskedToDo)
        # print 'Masked Done  : ' + str(maskedDone)

        todo = ((maskedToDo == 1))
        err  = ((maskedToDo != maskedDone))

        if err:
            print 'Prior error blocks execution!                                                              *   *   *   *   *   *   *   *   *'
            todo = False

        # print 'Do              : ' + str(todo)
        # print 'Error           : ' + str(err)
        # print '*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   '

        return todo

            
    def getCellsRange(self, worksheet, rangeDef):

        dictRange = {'rangeDef': rangeDef}
                
        dictRange['topLeft'] = rangeDef.partition(":")[0]
        dictRange['minRow'] = worksheet.get_int_addr(dictRange['topLeft'])[0]
        dictRange['minCol'] = worksheet.get_int_addr(dictRange['topLeft'])[1]

        dictRange['bottomRight'] = rangeDef.partition(":")[2]
        dictRange['maxRow'] = worksheet.get_int_addr(dictRange['bottomRight'])[0]
        dictRange['maxCol'] = worksheet.get_int_addr(dictRange['bottomRight'])[1]
        
        return dictRange
        
    def groupToArray(self, n, aList):
        regrouped = []
        row = []
        idx = 0
        for item in aList:
            if idx < n:
	        row.append(item)
                idx += 1
            else:
                regrouped.append(row)
                row = []
                row.append(item)
                idx = 1
            pass
        pass
        regrouped.append(row)
        
        return regrouped

    def right_most_column(self, rangeDef, wksht):
        return wksht.get_int_addr(rangeDef.partition(":")[2])[1]

    def dbIdFromExtId(self, ExtId, model):
        if self.modelIrModelData == None:
            self.setIrModelDataModel()
        return self.modelIrModelData.search_read([("name", "=", ExtId), ("model", "=", model)], ["res_id"])[0]["res_id"]

    def get_object_by_name(self, model, name):
        oerp = self.getConnection()
        id = oerp.search(model, [('name', 'ilike', name)])[0]
        return oerp.get(model).browse(id)

    def get_aliased_records(self, identifiers, model):
        oerp = self.getConnection()
        mapper = oerp.get(external_id_mapper)

        print oerp
        print external_id_mapper
        print model
        print identifiers

        mappings = oerp.search(external_id_mapper, [('name', 'in', identifiers), ('model', '=', model)])
        if len(mappings) == len(identifiers):
            ids = [mapper.browse(relation).res_id for relation in mappings]
            return oerp.get(model).browse(ids)

        known = [mapper.browse(relation).name for relation in mappings]
        missing = list(set(identifiers) - set(known))
        raise UnkownRecordError("In '{}' - no references found to {}".format(model, missing))


    def colNumsFromColNames(self, names):  # the array starts with the minCol title as zeroth element!
        titles = {}
        for title in names:
            titles[title] = names[title]
            print 'OErpModel >>>>>>>>>>>>>>>>>> Name : {}.  Number : {}.'.format(title, titles[title])
        
        return titles

    def title_row(self, limits, wksht):
        ret = {}
        row = wksht.row_values(1)
        idx = 0
        for col in row:
            idx += 1
            # print 'Col : {} @ {}'.format(col, idx)
            if idx >= limits['minCol'] and idx <= limits['maxCol']:
                ret[col] = idx

        return ret


    def getWorkingSource(self, parms):
        module_parms = {}
        module_parms['wkbk'] = self.gDataConnection.open_by_key(parms['docs_key'])
        module_parms['wksht'] = module_parms['wkbk'].worksheet(parms['docs_sheet'])

        module_parms['dictRange'] = self.getCellsRange(module_parms['wksht'], parms['data_range'])
        module_parms['numCols'] = self.right_most_column(module_parms['dictRange']['rangeDef'], module_parms['wksht'])
        module_parms['nameCol'] = self.title_row(module_parms['dictRange'], module_parms['wksht'])

        # print 'Column count is ' + str(module_parms['numCols'])

        return module_parms



    def load(self, parms, model):
        oerp = self.getConnection()

        print 'Loading to "{}".'.format(model)
        wkbk = self.gDataConnection.open_by_key(parms['docs_key'])
        wksht = wkbk.worksheet(parms['docs_sheet'])
        
        dictRange = self.getCellsRange(wksht, parms['data_range'])
        numCols = self.right_most_column(dictRange['rangeDef'], wksht)
        print 'Range is ' + str(numCols)


        fields = wksht.row_values(int(parms['titles_row']))[:numCols:]
        print ' - - - fields - - - '
        print fields
        
        data = self.groupToArray(numCols, [cell.value for cell in wksht.range(parms['data_range'])])
        print ' - - -  data  - - - '
        for item in data:
            print str(item)[:80]

        user_model = oerp.get(model)
        user_model.load(fields, data)

#        print 'Done in OErpModel'
        
    def parseSpecial(self, special):
        spec = special.lower()
        if spec.startswith('boolean'):
            if (spec[8] in "01"):
                if ("0" == spec[8]):
                    return False
                else:
                    return True
            else:
                return special
        elif spec.startswith('integer'):
            val = spec.strip('integer()')
            if val.lstrip("-+").isdigit():
                return int(val)
            else:
                return special
        elif spec.startswith('float'):
            val = spec.strip('float()')
            try:
                return float(val)
            except ValueError:
                return special
        else:
            return special 

        

    def testIt(self, task):
        getattr(lazyModule('models.' + task), task)().test("AAA")
        return

