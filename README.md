GData_OpenERP_Data_Pump
=======================

A very simple tool for feeding Google Spreadsheet data into the XMLRPC channel of OpenERP V7.

As much as possible, it uses third party tools:

- [gspread](https://pypi.python.org/pypi/gspread/)
- [openerplib](https://pypi.python.org/pypi/openerp-client-lib)
- [argparse](https://pypi.python.org/pypi/argparse)
- [Importing](http://peak.telecommunity.com/DevCenter/Importing)

This is an [overview diagram](https://docs.google.com/drawings/d/10hhX-2ChPynsfCaiQrNrt3eiy3m6j3Qz-0CF7NdnnQc).

This [detail diagram](https://docs.google.com/drawings/d/1Huy3CpSVM971iUX2M6bqBjjZIXES6SzchetloHjhy-I) shows the usage the pump makes of the columns in the controller sheets: *creds*, *task* and *parms*.

There is a sample [OpenErpGDataController](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdFdyc1NxOHN4eWZ6Q0lLMHVyWUpkaHc) an a sample [OpenErpGDataModel](https://docs.google.com/spreadsheet/ccc?key=0AiVG6SoU001RdE9BNnljbFVpa0xfazk0SUZOeWx1aEE)

The overall action is to:

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
    









