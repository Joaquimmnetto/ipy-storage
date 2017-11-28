"""Store and retrieve objects in IPython.

This module provides the public magics available to list, store and load
objects in IPython.

"""

import os
from ipystore.dillpickleshare import PickleShareDB


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
    try:
        #TODO: verificar o tamanho dos sets listados    
        result = [(o,0) for o in os.listdir(base_dir)
                if os.path.isdir(os.path.join(base_dir, o))]
    except FileNotFoundError as ex:
        raise FileNotFoundError(ex)
    
    return result