GData OpenERP Data Pump
=======================

<a name="Summary"/>
## [Summary](#Summary)

A very simple tool for feeding Google Spreadsheet data into the XMLRPC channel of OpenERP V7.

The goal is to facilitate controlling OpenERP instances from command line and DevOps tools (such as [http://jenkins-ci.org/](http://jenkins-ci.org/), [http://rundeck.org/](http://rundeck.org/), etc. )

As much as possible, it uses third party tools to hide the complexity of XMLRPC and Google's and OpenERP's APIs:

- [gspread](https://pypi.python.org/pypi/gspread/) - simplified wrapper to Google Spreadsheets API
- [openerplib](https://pypi.python.org/pypi/openerp-client-lib) - simplified wrapper to OpenERP API
- [argparse](https://pypi.python.org/pypi/argparse) - command line arguments organizer
- [Importing](http://peak.telecommunity.com/DevCenter/Importing) - delay code module import until required

The [overview diagram](https://docs.google.com/drawings/d/10hhX-2ChPynsfCaiQrNrt3eiy3m6j3Qz-0CF7NdnnQc) shows the main parts of the pump's operation.

This [detail diagram](https://docs.google.com/drawings/d/1Huy3CpSVM971iUX2M6bqBjjZIXES6SzchetloHjhy-I) shows the usage the pump makes of the columns in the controller sheets: *creds*, *tasks* and *parms*.

There is a sample controller ([OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc)) and a sample model ([OpenErpGDataModel](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdE9BNnljbFVpa0xfazk0SUZOeWx1aEE)) (TODO: test copying with Excel &/or Libre Office)

The overall action is a dispatcher within a dispatcher; the outer dispatcher instantiates classes named in column A of the *tasks* sheet while the inner dispatcher calls the _methods_ of the class that have been named in the *Action Step* cells of the same row.

[Top](#Contents)

<a name="Contents"/>
### Contents
#### [Introduction](#Introduction)
##### - [Currently Available Tasks](#Currently Available Tasks)
##### - [Main Steps](#Main Steps)
#### [First time execution](#First time execution)
#### [Minimal Module Example](#Minimal Module Example)
#### [Model Sheets](#Model Sheets)
##### - [ResCountryState example](#ResCountryState example)
##### - [ResUsers example](#ResUsers example)
#### [Repeat executions](#Repeat executions)
#### [Notes](#Notes)
##### - [Some useful documentation](#Some useful documentation)
##### - [Link to home site](#Link to home site)
##### - [Credits](#Credits)

- - - - - - - - - - - - -
<a name="Introduction"/>
## Introduction

<a name="Currently Available Tasks"/>
##### Currently Available Tasks

- database 		: create database
- ir.module.module 	: install_module
- base.language.install	: install language
- res.users 		: update record, bulk load
- res.country.state	: bulk load
- res.partner.category	: bulk load
- res.partner		: bulk load company, bulk load person
- res.partner.bank.type : bulk load
- res.partner.bank      : bulk load
- res.bank		: bulk load
- res.company		: bulk load
 
<a name="Main Steps"/>
##### Main Steps

In more detail, the action is:

1. connect to Google
1. connect to OpenERP using the credentials from the *creds* sheet
1. get a row from the *tasks* sheet
1. from the *parms* sheet, get the two-row range indicated in the *Parameter Block* cell of the *tasks* sheet row
1. instantiate the class specified by the *Model Class* column, passing in the above parameter block row
1. read from one of the *Action Step* columns the name of one the class's methods, only if the corresponding bit in the *Incomplete* bit map is set to 1, and the same bit in the *Complete* bit map is cleared to 0, otherwise skip to the next one. If both bits are 0 or both are 1, an error has occured
1. clear the *Incomplete* bit to 0
1. execute the indicated method
1. set the *Complete* bit to 1
1. repeat for each *Action Step* method, for as many as indicated in the *Length* cell
1. repeat for each *Model Class* 

The remote procedures you can call are documented here : [ORM and models](http://doc.openerp.com/trunk/developers/server/api_models/)

[Top](#Contents)



<a name="First time execution"/>
## First time execution


You will need to install the earlier mentioned third party tools:

    gspread
    openerplib
    argparse
    Importing

Please see the installation instructions in ["How to prepare prerequisites for the installation process."](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/wiki/Pre-install-steps)

The video [Google Spreadsheets to OpenERP Data Pump: Step #1 Installation](http://youtu.be/MEcNaHcp6Wg) might help.

You will have to make a private copy of the two examples ([OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc) and [OpenErpGDataModel](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdE9BNnljbFVpa0xfazk0SUZOeWx1aEE)).  Don't try to use the originals. It won't work.  The pump refers to the controller workbook by means of its search key and it, in turn, needs the search key of the model workbook.  Since you'll have made copies of both you'll need to be sure you use the correct keys.  


With that complete you can then run. . . 

    /opt/GData_OpenERP_Data_Pump$ ./pump.py

. . . to get . . . 

    usage: pump.py [-h] [-p USER_PWD] [-u USER_ID] key
    pump.py: error: too few arguments

The missing parameters are the access credentials for the [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc)

- [-u USER_ID] - Google user ID
- [-p USER_PWD] - Google user password 
- key - the spreadsheet key taken from URL of the spreadsheet. Eg: "0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc"

Thus a valid call would be . . . 

    /opt/GData_OpenERP_Data_Pump$ ./pump.py -u yourgoogleid -p yourgooglepwd "0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc"
    
However, to avoid UID and PWD from appearing in the command line, `pump.py` will record those values in the file `.gdataCreds` that has the form :

    {"user_id": "yourgoogleid", "user_pwd": "yourgooglepwd"} 

When that file exists the command line can be, simply . . . 

    /opt/GData_OpenERP_Data_Pump$ ./pump.py "0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc"
    
See the section *Repeat Execution* below to learn how to get fine grained control of which *Action Steps* are executed or skipped.

[Top](#Contents)




<a name="Minimal Module Example"/>
## Minimal Module Example


There is a [minimal example](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/blob/master/models/MinimalModuleExample.py) with a single method, in GitHub, which the [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc) example uses.

The design of the pump allows you to add easily, one or more of your own *Model Class* handlers.  They will inherit from `./models/OErpModel.py` Everything that can be handled in the parent class of the handlers **is** handled there.  Apart from the few print statements, there are no unnecessary lines.  A few things have to be done in the child classes so a small amount of code duplication results.  

The best way to make a new one is to adapt the *Minimal Module Example* to your needs.

In the spreadsheets, it's easiest and safest to copy the MinimalModuleExample rows and edit them. Pay attention to which cells have formulas (grey background); you don't want to alter them.

You have to make sure of four things:

1. there is a row in the *tasks* sheet that has the name of your class in column A
1. the names in the *Action Step* columns in that row match the names of methods of your class
1. there is a 2-row parameter block in the *parms* sheet with keys above and values below that are understood by your class methods
1. the *Parameter Block* cell correctly identifies the 2-row range


The customization steps are:

- Search for "MinimalModuleExample", and replace all with your module name.
- If you will be referring to a single OpenERP model, name it in the line beginning: `OPENERP_MODULE_NAME = `
- Every new method you create (similar to `def chkTask(self, parms):`) must have an entry in the dictionary `self.methods` that is initialized in the `__init__(self)` method and used in the line `self.methods[aMethod](self.parameters)`

[Top](#Contents)



<a name="Model Sheets"/>
## Model Sheets
------------

Based on the pattern of loading name/value pairs into a dictionary, and passing the dictionary to a method, there is really no limit to what the called method can be made to do.

Note: The *parms* sheet and Python code could be made more intelligent about deriving row and column ranges from source data sheets.  Rightly or wrongly, I decided that it was wise to leave that responsibility with users. 

[Top](#Contents)



<a name="ResCountryState example"/>
### ResCountryState example

[ResCountryState.py](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/blob/master/models/ResCountryState.py) provides a complete example of a high speed data load operation. The goal is to collect the correct data for the `openerplib` command `user_model.load(fields, data)`.

In the *tasks* sheet, of [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc), the row containing the class name `ResCountryState` provides the method to be called (`load`) and the range in the *parms* sheet where the parameters for `load` can be found.  In the *tasks* sheet, the row containing the class name `ResCountryState` provides the key names, and the following row provides the values, to be added to the dictionary that will be passed to `load`.

The keys/values have the following signfications:

- `docs_key`/"0AiVG6SoU001RdE9BNnljbFVpa0xfazk0SUZOeWx1aEE" - The key to the Google Spreadsheet holding the data to be loaded.
- `docs_sheet`/"res.country.state" - The name of the exact sheet holding the data to be loaded.
- `titles_row`/"1" - The number of the row holding model attribute titles as specified in OpenERP.
- `range`/"A2:C14" - The range of cells (13 rows : 3 columns) holding the data to be loaded.


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

		# Get the model for loading . . . 
        user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)

        # . . . and load it.
        user_model.load(fields, data)

[Top](#Contents)




<a name="ResUsers example"/>
### ResUsers example


The class in [ResUsers.py](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/blob/master/models/ResUsers.py) shows a simple update of a single model record.  It has no need to pull lots of data, so the *parms* page can provide what is needed directly.

    def update(self, parms):
               
        # Will update the OpenERP model 'res.user'
        user_model = OErpModel.openErpConnection.get_model(OPENERP_MODULE_NAME)

        # Obtain an array of record ids that match the selection criteria (only one in this case)
        thisUser = user_model.search([("login", "=", parms['login'])])[0]

        # Read the existing data (only what we need)
        nameUser = user_model.read(thisUser, ["name"])["name"]
        print "Login " + parms['login'] + " -- " + nameUser

        # Write it back out with update applied
        for key  in parms:
            if key not in ("ResUsers", "login"):    # Ignore the record key attribute
                val = OErpModel.parseSpecial(self, parms[key]) 
                print 'Writing : (User : {}, "{}":"{}") from "{}"'.format(nameUser, key, val, parms[key])
                user_model.write(thisUser, {key:val})
                print 'Written'

[Top](#Contents)



<a name="Repeat executions"/>
## Repeat executions

In each child class of `OErpModel.py` there should be calls to the parent class methods, `starting` and `finished` just before and just after the call to an *Action Step*, like this:

    super(MinimalModuleExample, self).starting(idx)

    self.methods[aMethod](self.parameters)

    super(MinimalModuleExample, self).finished(idx)

These calls update the *Bit Maps* cells *Complete* and *Incomplete*.

You can set the values in those two columns manually, but keep an eye on the last four *Binary* columns.

They don't actually do anything, instead they are there to aid in seeing whether the right bits are set to enable only the required *Action Steps*.  The Pump itself also modifies those cells, clearing the *Incomplete* bit to 0, when starting an *Action Step*, and setting the *Complete* bit to 1 when the *Action Step* is finished.

The *Chk* column will turn red and indicate a discrepancy if the *Complete* and *Incomplete* bits do not add up to the *Length* value.  If you set those values with a discrepancy yourself, and ignore the red flag, then the Pump will throw an error when you run it.  Also, if a discrepancy shows after the Pump ran, then you know it experienced some other sort of error and could not complete the indicated step.

The execution of an example  with five *Action Steps* and *Complete* and *Incomplete* set to 27 and 4 respectively would produce a result log file like this:

    Task#1 uses the module "MinimalModuleExample".
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Processing task #1
    Task parameters found in range "A4:B5".
        #1 Skipping "chkTask"!
        #2 Skipping "chkTask"!
        #3 Doing "chkTask" now.
    Task check for key "first_parm" found : "dummy"!
    __
        #4 Skipping "chkTask"!
        #5 Skipping "chkTask"!
[Top](#Contents)


<a name="Notes"/>
## Notes

<a name="Some useful documentation"/>
### Some useful documentation

- for the db service:
  - [http://pythonhosted.org/OERPLib/tutorials.html](http://pythonhosted.org/OERPLib/tutorials.html)
  - [http://pythonhosted.org/OERPLib/ref_db.html#oerplib.service.db.DB](http://pythonhosted.org/OERPLib/ref_db.html#oerplib.service.db.DB)
- for other Google & OpenERP connectivity
  - [http://www.youtube.com/playlist?p=PLq7op4J183lX44ZlXPiHxUpRvmmRDtxye](http://www.youtube.com/playlist?p=PLq7op4J183lX44ZlXPiHxUpRvmmRDtxye)
- Pre-install-steps
  - [How to prepare prerequisites for the installation process.](https://github.com/martinhbramwell/GData_OpenERP_Data_Pump/wiki/Pre-install-steps#how-to-prepare-prerequisites-for-the-installation-process)

<a name="Link to home site"/>
### Link to home site
http://martinhbramwell.github.io/GData_OpenERP_Data_Pump

<a name="Credits"/>
### Credits 

1. Some ideas pilfered from here [https://gist.github.com/t3dev/3016471](https://gist.github.com/t3dev/3016471)
2. Code developed and run on a ´KVM 7´ from the **so_great_you_cannot_believe_it** VPS service of [https://www.prometeus.net/billing/cart.php?gid=13](https://www.prometeus.net/billing/cart.php?gid=13)
3. Editing done through the **really cool** browser based IDE [https://github.com/mattpass/ICEcoder](https://github.com/mattpass/ICEcoder)

[Top](#Contents)

