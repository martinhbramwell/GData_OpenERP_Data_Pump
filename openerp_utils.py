#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-11-25

@author: Martin H. Bramwell
'''

import oerplib, sys
import socket

from models.OErpModel import OErpModel

class OpenERP(object):

    def __init__(self, credentials):
        print "Getting connection to {} for {}".format(credentials['db_name'], credentials['user_id'])
	try:
	    oerp = oerplib.OERP(server=credentials['host_name'], protocol='xmlrpc', port=credentials['host_port'])
	    OErpModel.openErpConnection['super'] = oerp
	    if credentials['db_name'] in oerp.db.list():
	        db_connect(credentials['user_id'], credentials['user_pwd'], credentials['db_name'])
	    else:
	        print "There is no database called : {}".format(credentials['db_name'])
	except socket.gaierror:
	    sys.exit("Is this the correct URL : {}".format(credentials['host_name']))
	except socket.error:
	    sys.exit("Is this the correct port number : {}".format(credentials['host_port']))

def db_connect(usr, pwd, db):
    oerp = OErpModel.openErpConnection['super']
    user = oerp.login(user=usr, database=db, passwd=pwd)
    OErpModel.openErpConnection['admin'] = user
    # print " - - {} - - ".format(user)

