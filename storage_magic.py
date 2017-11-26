"""Store and retrieve objects in IPython.

This module provides the public magics available to list, store and load
objects in IPython.
"""

"""%sets:
Operations with sets. Create/Open or destroy sets, change the current base directory, or list the existing sets.
    %sets [base_dir] - List the exsisting sets
    %sets -o [set_name] [base_dir='./ipy_db'] - Create/Open a set
    %sets -d [set_name=current] [base_dir='./ipy_db'] - Destroy a set
    %sets -b [base_dir] - Change the base directory to base_dir
"""


"""%setstore:
Operations within a set. save, load or delete values and list the set current contents.
    %setstore - List the objects currently stored in the set
    %setstore -s [items_to_save] - save items in the current set (multiple items must be comma-separated)
    %setstore -sa - save all items in the namespace with a corresponding name in the current set
    %setstore -l [items_to_load] - load items from the current set (multiple items must be comma-separated)
    %setstore -la  - load all items from the current set
    %setstore -d [items_to_delete] - delete items in the current set (multiple items must be comma-separated)    
"""

import os

from IPython import get_ipython
from IPython.core.magic import Magics, magics_class, line_magic

from dillpickleshare import PickleShareDB
from argparse import ArgumentParser

from storage import StorageSet, list_sets

def _unpack_args(args, count, *defaults):
    results = []
    for i in range(count):
        try:
            value = args.pop(0)
        except IndexError:
            value = defaults[i]
        results.append(value)

    return tuple(results)

@magics_class
class SetStoreMagics(Magics):
    def __init__(self, shell, data=None):
        super(SetStoreMagics, self).__init__(shell)
        self.ip = shell
        self.def_base = "./ipy_db"
        self.current_set = None
        self.db = None
        
    @line_magic
    def sets(self, args):
        """ Manages the %sets magic, that can open, delete and list sets.            
        """
        args = ' '.join([for s in args.split(' ') if len(s) > 0])
        comm = args.pop(0)

        if comm == '-o':            
            set_name, base_dir = _unpack_args(args, 2, None, self.def_base)
            self.current_set = StorageSet(set_name, base_dir)

        elif comm == '-d':
            set_name, base_dir = _unpack_args(args, 2, None, self.def_base)
            to_delete = self.current_set            
            if set_name is None and self.current_set is None:
                print("Open or name a set in order to destroy it.")
                return                
            elif set_name is not None:                
                to_delete = StorageSet(self.ip, set_name, base_dir)
            to_delete.remove_set()

        elif comm == '-b':
            base_dir = _unpack_args(args, 1)
            if base_dir is None:
                print("Current base dir is: {}".format(self.def_base))
            else:
                self.def_base = base_dir            
        
        else:
            base_dir = _unpack_args(args, 1, self.def_base)
            print("Sets at {}:".format(self.def_base))
            for set_name,set_size in list_sets(base_dir):
                print("{},{}".format(set_name,set_size))

     @line_magic
    def setstore(self, args):
        """Manages the %setstore magic, responsible to save, load, delete and list objects in the current set.        
        """
        if self.db is None:
            print("Open a set first, available sets:")
            print(self.listsets())
            return

        args = ' '.join([for s in args.split(' ') if len(s) > 0]
        comm = args.pop(0)

        if comm == "-s" or comm == "-sa":            
            if comm == "-s":
                if len(args == 0):
                    print("Please list the objects that you desire to be stored"
                    print("e.g. %setstore foo,bar")
                    return
                items = args.strip().split(",")
            else:
                items = [n for n,s self.current_set.list_contents()]

            self.current_set.store(items)
            print("Stored {} items".format(len(items)))
        
        if comm == "-l" or comm == "-la":
            if comm == "-l":
                if len(args == 0):
                    print("Please list the objects that you desire to be loaded"
                    print("e.g. %setstore foo,bar")
                    return
                items = args.strip().split(",")
            else:
                items = [n for n,s self.current_set.list_contents()]
            self.current_set.load(items)
            print("Loaded {} items".format(len(items)))

        if comm == "-d":
             if len(args == 0):
                print("Please list the objects that you desire to be loaded"
                print("e.g. %setstore foo,bar")
                return
            items = args.strip().split(",")
            self.current_set.delete(items)
            print("Deleted {} items".format(len(items)))
        
        else:
            print("Objects currently in the {} set".format(self.current_set.name))
            total_size = 0
            for obj,size in self.current_set.list_contents():
                print("{} \t {} bytes".format(obj,size))
                total_size += size
            print("Total size: {} bytes".format(total_size))
        
    
ip = get_ipython()
ip.register_magics(SetStoreMagics(ip, None))
