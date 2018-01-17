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

from ipystore.storage import StorageSet, list_sets

silent = True #TODO: Yeah, this is awful and should be a config. option or smth.
def log(x): 
    if not silent:
        print(x)

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
        
    @line_magic
    def sets(self, args):
        """ Manages the %sets magic, that can open, delete and list sets.            
        """
        args = [arg for arg in args.split(' ') if len(arg) > 0]
        if len(args) > 0:
            comm = args.pop(0)
        else:
            comm = ""

        if comm == '-o':            
            set_name, base_dir = _unpack_args(args, 2, None, self.def_base)
            self.current_set = StorageSet(self.ip, set_name, base_dir)
            log("Set {} opened".format(set_name))

        elif comm == '-d':
            set_name, base_dir = _unpack_args(args, 2, None, self.def_base)
            to_delete = self.current_set            
            if set_name is None and self.current_set is None:
                log("Open or name a set in order to destroy it.")
                return                
            elif set_name is not None:                
                to_delete = StorageSet(self.ip, set_name, base_dir)
            to_delete.remove_set()
            log("Set {} removed".format(set_name))            

        elif comm == '-b':
            base_dir, = _unpack_args(args, 1)
            if base_dir is None:
                log("Current base dir is: {}".format(self.def_base))
            else:
                self.def_base = base_dir
                log("New base dir is {}.".format(self.def_base))
        else:
            base_dir = comm if comm!="" else self.def_base
            try:
                log("Sets at {}:".format(base_dir))
                for set_name,set_size in list_sets(base_dir):
                    log("{},{}".format(set_name,set_size))
            except KeyError:
                log("Directory {} does not exists".format(base_dir))

    @line_magic
    def setstore(self, args):
        """Manages the %setstore magic, responsible to save, load, delete and list objects in the current set.        
        """
        if self.current_set is None:
            log("Open a set first, available sets at {}:".format(self.def_base))
            log(list_sets(self.def_base))
            return

        args = [arg for arg in args.split(' ') if len(arg) > 0]                        
        if len(args) > 0:
            comm = args.pop(0)
        else:
            comm = ""
        args = ''.join(args).split(' ')        

        if comm == "-s" or comm == "-sa":            
            if comm == "-s":
                if len(args) == 0:
                    log("Please list the objects that you desire to be stored")
                    log("e.g. %setstore foo,bar")
                    return
                items = args.pop(0).strip().split(",")
            else:
                items = [n for n,s in self.current_set.list_contents()]

            self.current_set.store(items)
            log("Stored {} items".format(len(items)))
        
        elif comm == "-l" or comm == "-la":
            if comm == "-l":
                if len(args) == 0:
                    log("Please list the objects that you desire to be loaded")
                    log("e.g. %setstore foo,bar")
                    return
                items = args.pop(0).strip().split(",")
            else:                
                items = [n for n,s in self.current_set.list_contents()]
            try:
                self.current_set.load(items)
                log("Loaded {} items".format(len(items)))
            except KeyError:
                log("Item not present in the current set")

            

        elif comm == "-d":
            if len(args) == 0:
                log("Please list the objects that you desire to be loaded")
                log("e.g. %setstore foo,bar")
                return
            items = args.pop(0).strip().split(",")
            try:
                self.current_set.delete(items)
                log("Deleted {} items".format(len(items)))
            except FileNotFoundError:
                log("Item not present in the current set")

        else:
            log("Objects currently in the {} set".format(self.current_set.name))
            total_size = 0
            for obj,size in self.current_set.list_contents():
                log("{} \t {} bytes".format(obj,size))
                total_size += size
            log("Total size: {} bytes".format(total_size))
        
def load_ipython_extension(ip, **kwargs):
    ip = get_ipython()
    ip.register_magics(SetStoreMagics(ip, None))
