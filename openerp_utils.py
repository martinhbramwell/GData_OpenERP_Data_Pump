#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-11-25

@author: Martin H. Bramwell
'''

import oerplib
import sys
import socket

from models.OErpModel import OErpModel


class OpenERP(object):

    def __init__(self, credentials):
        db = credentials['db_name']
        user_id = credentials['user_id']
        host_name = credentials['host_name']
        host_port = credentials['host_port']
        user_pwd = credentials['user_pwd']

        print "Getting connection to {} for {}".format(db, user_id)
        try:
            oerp = oerplib.OERP(
                server=host_name, protocol='xmlrpc', port=host_port)
            OErpModel.openErpConnection['super'] = oerp
            if db in oerp.db.list():
                db_connect(user_id, user_pwd, db)
            else:
                print "There is no database called : {}".format(db)
        except socket.gaierror:
            sys.exit(
                "Is this the correct URL : {}".format(host_name))
        except socket.error:
            sys.exit(
                "Is this the correct port number : {}".format(host_port))


def db_connect(usr, pwd, db):
    oerp = OErpModel.openErpConnection['super']
    user = oerp.login(user=usr, database=db, passwd=pwd)
    OErpModel.openErpConnection['admin'] = user
    # print " - - {} - - ".format(user)
