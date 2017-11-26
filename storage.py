import os
from dillpickleshare import PickleShareDB

from IPython import get_ipython
from IPython.core.magic import Magics, magics_class, line_magic


ip = get_ipython()

#%listsets -> list_sets (list all folders with in the db folder)
#%setopen [set_name] [items_to_load] -> open_set
#%setload [items_to_load][from_set] -> load_items
#%setload [-a] -> load all items from the current set
#%setstore [items_to_store][to_set] -> add_items

#Alternativas:
#funciona com %load mas não funciona com %run
#não funciona com import

def sets_list(base_dir):
  d = base_dir  
  set_list = [o for o in os.listdir(d) 
                    if os.path.isdir(os.path.join(d,o))]

  return set_list

def set_load(items, ip=None, db=None, all=False):
  if all:
    items = list(db.keys())
  
  for item in items:
    ip.user_ns[item] = db[item]   
  

def set_store(items, ip=None, db=None):
  for item in items:
    obj = ip.user_ns[item]
    try:
      db[item] = obj
    except KeyError:
      print("Item ",item," is not available in the set")

def set_objects(db=None):
  return

@magics_class
class SetStoreMagics(Magics):

  def __init__(self,shell,data=None):
    super(SetStoreMagics, self).__init__(shell)    
    self.ip = shell
    self.base_dir = "./ipy_db"
    self.db = None

  @line_magic
  def setopen(self, args):
    """
    Create a new or open a existing set         \n
      %setopen [set_name] [base_dir='./ipy_db'] \n
      %setopen myset mydata                     \n
      %setopen myset 
    """
    base = self.base_dir
    args = args.split(' ')
    if len(args) == 1:
      set_name = args[0]
    else:
      base = args[1]
    
    dir_path = os.sep.join([self.base_dir, set_name])
    if not os.path.isdir(dir_path):
      os.makedirs(dir_path)
  
    self.db = PickleShareDB(dir_path)

  @line_magic
  def listsets(self,base=""):
    """
      List all sets available in the given base dir \n
      %listsets [base_dir='./db'] \n
      eg. %listsets mydb          \n
          %listsets               \n
    """
    if base == "":
      base = self.base_dir

    print("Listing sets at",base)
    
    for set_dir in sets_list(base):
      print(set_dir)

  @line_magic
  def setload(self, args):
    """
      Load objects from the opened set.       \n
      %setload [items_to_load]                \n
      eg. %setload bar,foo,func               \n
      Or, load all files from the current set.\n
      %setload [-a]                           \n

    """
    if self.db is None:
      print("Open a set first, available sets:")
      print(self.listsets())
      return None;      

    if args == "-a":
      items = None
      all = True
      pass
    else:
      items = args.split(",")
      all = False
    
    set_load(items, ip = self.ip, db = self.db, all=all)
    print("Values loaded sucessfully")

  @line_magic
  def setstore(self, args):
    """
      Store one or more objects in the opened set.  \n
      %setstore [items_to_store]                    \n
      eg. %setstore foo,bar,func                    \n
    """
    if self.db is None:
      print("Open a set first, available sets:")
      print(self.listsets())
    
    items = args.split(",")
    set_store(items, ip=self.ip, db=self.db)

    print("Values stored sucessfully")

  @line_magic
  def setobjs(self, args):
    if args != '':
      db = PickleShareDB(args)
    elif self.db is not None:
      db = self.db
    else:
      print("Open a set first, available sets:")
      print(self.listsets())
      return None

    objs = sorted(list(db.keys()))
    print("Objects in ",db.root,":")
    for obj in objs:
      print(obj)







# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip = get_ipython()
ip.register_magics(SetStoreMagics(ip,None))

