import os

from IPython import get_ipython
from IPython.core.magic import Magics, magics_class, line_magic

from dillpickleshare import PickleShareDB


ip = get_ipython()

"""
%listsets -> list_sets (list all folders with in the db folder)
%setopen [set_name] [items_to_load] -> open_set
%setload [items_to_load][from_set] -> load_items
%setload [-a] -> load all items from the current set
%setstore [items_to_store][to_set] -> add_items
"""

"""
Alternatives:
It works with %load, but not with %run.
It does not work with import either.
"""


def sets_list(base_dir):
    d = base_dir
    set_list = [o for o in os.listdir(d)
                if os.path.isdir(os.path.join(d, o))]

    return set_list


def set_load(items, ip=None, db=None, load_all=False):
    if load_all:
        items = list(db.keys())
    for item in items:
        ip.user_ns[item] = db[item]


def set_store(items, ip=None, db=None):
    for item in items:
        obj = ip.user_ns[item]
        try:
            db[item] = obj
        except KeyError:
            print("Item {} is not available in the set.".format(item))


def set_objects(db=None):
    raise NotImplementedError()


@magics_class
class SetStoreMagics(Magics):
    def __init__(self, shell, data=None):
        super(SetStoreMagics, self).__init__(shell)
        self.ip = shell
        self.base_dir = "./ipy_db"
        self.db = None

    @line_magic
    def setopen(self, args):
        """Create a new or open a existing set.

        %setopen [set_name] [base_dir='./ipy_db']
        %setopen myset mydata
        %setopen myset
        """
        base = self.base_dir  # base is never used.
        args = args.split()
        if len(args) == 1:
            set_name = args[0]
        else:
            base = args[1]  # base is never used.

        dir_path = os.sep.join([self.base_dir, set_name])
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        self.db = PickleShareDB(dir_path)

    @line_magic
    def listsets(self, base=""):
        """List all sets available in the given base dir.

        %listsets [base_dir='./db']
        eg. %listsets mydb
        %listsets
        """
        if not base:
            base = self.base_dir

        print("Listing sets at {}".format(base))

        for set_dir in sets_list(base):
            print(set_dir)

    @line_magic
    def setload(self, args):
        """Load objects from the opened set.

        %setload [items_to_load]
        eg. %setload bar,foo,func
        Or, load all files from the current set
        %setload [-a]
        """
        if self.db is None:
            print("Open a set first, available sets:")
            print(self.listsets())

            return None

        if args == "-a":
            items = None
            load_all = True
        else:
            items = args.split(",")
            load_all = False

        set_load(items, ip=self.ip, db=self.db, load_all=load_all)
        print("Values loaded sucessfully")

    @line_magic
    def setstore(self, args):
        """Store one or more objects in the opened set.
        %setstore [items_to_store
        eg. %setstore foo,bar,func
        """
        if self.db is None:
            print("Open a set first, available sets:")
            print(self.listsets())

        items = args.split(",")
        set_store(items, ip=self.ip, db=self.db)

        print("Values stored sucessfully")

    @line_magic
    def setobjs(self, args):
        if args:
            db = PickleShareDB(args)
        elif self.db is not None:
            db = self.db
        else:
            print("Open a set first, available sets:")
            print(self.listsets())

            return None

        objs = sorted(list(db.keys()))
        print("Objects in {}:".format(db.root))
        for obj in objs:
            print(obj)


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip = get_ipython()
ip.register_magics(SetStoreMagics(ip, None))
