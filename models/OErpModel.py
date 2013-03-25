#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-03-19

@author: Martin H. Bramwell
'''

class OErpModel(object):

    openErpConnection = None
    gDataConnection = None
    
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

        
    def starting(self, idx):
        # print 'Starting #' + str(idx)
        bit = ((self.mask -1) << idx) & self.mask
        col = 1 + OErpModel.CONSTANTS['INCOMPLETION_MAP']
        row = self.currentRow

        incomplete = int(self.shtTasks.cell(row, col).value)    # cell(row, col)
        self.shtTasks.update_cell(row, col, bit & incomplete)   # update_cell(row, col, value)
        # print 'Cleared bit #' + str(bit) + '(with ' + str(bit & incomplete) + ') in column #' + str(col) + ' and row #' + str(row)

    def finished(self, idx):
        # print 'Finished #' + str(idx)
        bit = 1 << idx
        col = 1 + OErpModel.CONSTANTS['COMPLETION_MAP']
        row = self.currentRow

        incomplete = int(self.shtTasks.cell(row, col).value)    # cell(row, col)
        self.shtTasks.update_cell(row, col, bit | incomplete)   # update_cell(row, col, value)

        # print 'Set the bit #' + str(bit) + '(with ' + str(bit | incomplete) + ') in column #' + str(col) + ' and row #' + str(row)

        

        
    def process(self, wrksht, rowTask):
    
        print 'Processing task #' + str(rowTask - 1)
        self.currentRow = rowTask
        
        self.shtTasks = wrksht.worksheet("Tasks")
        shtParms = wrksht.worksheet("Parms")

        self.task_parms = self.shtTasks.row_values(rowTask)
        # print 'Task parameters found in range "{}".'.format(self.task_parms[1])
        
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
            print 'Prior error blocks execution! '
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




