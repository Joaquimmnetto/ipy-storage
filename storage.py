"""Store and retrieve objects in IPython.

This module provides the public magics available to list, store and load
objects in IPython.

The main magics and their respective functions are the following
(magic [options]: description -> function):

%listsets : list all folders with in the db folder -> list_sets
%setopen [set_name] [items_to_load] -> open_set
%setload [items_to_load] [from_set] -> load_items
%setload [-a] : load all items from the current set -> set_load
%setstore [items_to_store][to_set] -> add_items
"""

import os
from IPython import get_ipython
from dillpickleshare import PickleShareDB


class StorageSet():

    def __init__(self, shell, set_name, base_dir):
        dir_path = os.sep.join([base_dir, set_name])
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        self.db = PickleShareDB(dir_path)
        self.ip = shell
        self.name = set_name

    def list_contents(self):
        #TODO: pegar o tamanho dos items (tamanho do arquivo, ou carregar o item para saber o tamanho dele na heap?)
        return [(n,0) for n in sorted(self.db.keys())]

    def store(self, items):
        for item in items:
            obj = self.ip.user_ns[item]
            self.db[item] = obj

    def load(self, items):        
        for item in items:
            self.ip.user_ns[item] = self.db[item]

    def delete(self, items):
        for item in items:
            del(self.db[item])

    def remove_set(self):
        self.db.clear()
        os.rmdir(self.db.root)    


def list_sets(base_dir):    
    #TODO: verificar o tamanho dos sets listados
    return [(o,0) for o in os.listdir(base_dir)
                if os.path.isdir(os.path.join(base_dir, o))]
    