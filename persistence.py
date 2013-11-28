#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-11-25

@author: Martin H. Bramwell
'''

import os
import stat
import shelve

# This is the shelve file where our OAuth arguments persist between executions
store = {}
store_file = '.credStore.db'
store_path = os.path.expanduser('~') + '/' + store_file


def close_store():
    """ Remove the 'shelve' daemon from memory.
"""
    if store :
        store.close()

def make_store():
    """ Create a 'shelve' repository.
"""
    global store
    store = shelve.open(store_path, writeback = True)
    os.chmod(store_path, stat.S_IRUSR | stat.S_IWUSR)
    return store
    
def reopen_store():
    close_store()
    return make_store()

def drop_store():
    os.remove(store_path)



