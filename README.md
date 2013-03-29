GData_OpenERP_Data_Pump
=======================

A very simple tool for feeding Google Spreadsheet data into the XMLRPC channel of OpenERP V7.

As much as possible, it uses third party tools:

- [gspread](https://pypi.python.org/pypi/gspread/) - simplified wrapper to Google Spreadsheets API
- [openerplib](https://pypi.python.org/pypi/openerp-client-lib) - simplified wrapper to OpenERP API
- [argparse](https://pypi.python.org/pypi/argparse) - command line arguments organizer
- [Importing](http://peak.telecommunity.com/DevCenter/Importing) - delay code module import until required

This is an [overview diagram](https://docs.google.com/drawings/d/10hhX-2ChPynsfCaiQrNrt3eiy3m6j3Qz-0CF7NdnnQc) to show the main parts of the pump's operation.

This [detail diagram](https://docs.google.com/drawings/d/1Huy3CpSVM971iUX2M6bqBjjZIXES6SzchetloHjhy-I) shows the usage the pump makes of the columns in the controller sheets: *creds*, *tasks* and *parms*.

There is a sample controller ([OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc)) and a sample model ([OpenErpGDataModel](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdE9BNnljbFVpa0xfazk0SUZOeWx1aEE))

The overall action is a dispatcher within a dispatcher; the outer dispatcher instantiates classes named in column A of the *tasks* sheet while the inner dispatcher calls methods on the class named in the *Action Step* cells of the same row.

In more detail, the action is:

1. connect to Google
1. connect to OpenERP using the credentials from the *creds* sheet
1. get a row from the *tasks* sheet
1. from the *parms* sheet, get the two-row range indicated in the *Parameter Block* cell of the *tasks* sheet row
1. instantiate the class specified by the *Model Class* column, passing in the above parameter block row
1. read from one of the *Action Step* columns the name of one the class's methods, if the corresponding bit in the *Incomplete* bit map is 1, and the same bit in the *Complete* bit map is 0, otherwise skip to the next one. If both bits are 0 or both are 1, an error has occured
1. set the *Incomplete* bit to 0
1. execute the indicated method
1. set the *Complete* bit to 1
1. repeat for each *Action Step* method, for as many as indicated in the *Length* cell
1. repeat for each *Model Class* 

First time execution
--------------------

You will need to install the earlier mentioned third party tools:

    sudo easy_install gspread
    sudo easy_install openerplib
    sudo easy_install argparse
    sudo easy_install Importing


You can then run . . . 

    /opt/GData_OpenERP_Data_Pump$ ./gDataTools.py

. . . to get . . . 

    usage: gDataTools.py [-h] [-p USER_PWD] [-u USER_ID] key
    gDataTools.py: error: too few arguments

The missing parameters are the access credentials for the [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc)

- [-u USER_ID] - Google user ID
- [-p USER_PWD] - Google user password 
- key - the spreadsheet key taken from URL of the spreadsheet. Eg: "0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc"

Thus a valid call would be . . . 

    /opt/GData_OpenERP_Data_Pump$ ./gDataTools.py -u yourgoogleid -p yourgooglepwd "0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc"
    
However, to avoid UID and PWD from appearing in the command line, `gDataTools.py` will record those values in the file `.gdataCreds` that has the form :

    {"user_id": "yourgoogleid", "user_pwd": "yourgooglepwd"} 

When that file exists the command line can be, simply . . . 

    /opt/GData_OpenERP_Data_Pump$ ./gDataTools.py "0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc"
    

Minimal Module Example
----------------------

The design of the pump allows you to add easily, one or more of your own *Model Class* handlers.  You have to make sure of three things:

1. there is a row in the *tasks* sheet that has the name of your class in column A.
2. the names in the *Action Step* columns in that row match the names of methods of your class
3. there is a 2 row parameter block in the parms with keys above and values below that are understood by your class methods.

There is a [minimal example](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/blob/master/models/MinimalModuleExample.py) in GitHub, referred to in the [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc) example.  Everything that can be handled in the parent class **is** handled there.  Apart from the few print statements, there are no unnecessary lines.

The customization steps are:

- Search for "MinimalModuleExample", and replace all with your module name.
- If you will be referring to a single OpenERP model, name it in the line beginning: `OPENERP_MODULE_NAME = `
- Every new method you create (dimilar to `def chkTask(self, parms):`) must have an entry in the dictionary `self.methods` that is initialized in the `__init__(self)` method and used in the line `self.methods[aMethod](self.parameters)`



Model Sheets
------------

Based on the pattern of loading name/value pairs into a dictionary, and passing the dictionary to a method, there is really no limit to what the called method can be made to do.

[ResCountryState.py](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/blob/master/models/ResCountryState.py) provides a complete example of a high speed data load operation. The goal is collect the correct data for the `openerplib` command `user_model.load(fields, data)`.

In the *tasks* sheet, of [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc), the row containing the class name `ResCountryState` provides the method to be called (`load`) and the range in the *parms* sheet where the parameters for `load` can be found.  In the *tasks* sheet, the row containing the class name `ResCountryState` provides the key names, and the following row provides the values, to be added to the dictionary that will be passed to `load`.

The keys/values have the following signfications:

- `docs_key`/"0AiVG6SoU001RdE9BNnljbFVpa0xfazk0SUZOeWx1aEE" - The key to the Google Spreadsheet holding the data to be loaded.
- `docs_sheet`/"res.country.state" - The name of the exact sheet holding the data to be loaded.
- `titles_row`/"1" - The number of the row holding model attribute titles as specified in OpenERP.
- `range`/"A2:C14" - The range of cells (12 rows : 3 columns) holding the data to be loaded.


The code is as follows :

    def load(self, parms):

        # Loading to the OpenERP model 'res.country.state'
        wkbk = OErpModel.gDataConnection.open_by_key(parms['docs_key'])

        # Obtaining data from the sheet 'res.country.state' . . . 
        wksht = wkbk.worksheet(parms['docs_sheet'])

        # . . . in the range A2:C14
        dictRange = super(ResCountryState, self).getCellsRange(wksht, parms['range'])
                
        # With titles from the first row of the sheet . . . 
        fields = wksht.row_values(int(parms['titles_row']))

        # . . . and data from ensuing rows
        data = super(ResCountryState, self).groupToArray(3, [cell.value for cell in wksht.range(parms['range'])])
        for idx in range(4):
            print data[idx]

		# Get the model for loading . . . 
        user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)

        # . . . and load it.
        user_model.load(fields, data)









