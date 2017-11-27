import unittest

from dillpickleshare import PickleShareDB
from storage import StorageSet,list_sets

#"""ipython -i -c "%run test.py 1 2 3 4""""

def mock_function():
    pass

class StorageSetTest(unittest.TestCase):

    def setUp(self):
      self.base_dir = 'temp'
      self.shell = get_ipython()

    def test_list_sets(self):
        
        obj_sets = [StorageSet(self.shell, 'temp', self.base_dir), StorageSet(self.shell, 'temp2', self.base_dir), 
                    StorageSet(self.shell, 'temp3', self.base_dir)]
        sets = list_sets(self.base_dir)
        assert len(sets) == len(obj_sets) and len(sets[0]) == 2

        for obj in obj_sets:
            obj.remove_set()        

    def test_persist_single_item(self):
        obj_set = StorageSet(self.shell, 'temp', self.base_dir)
        store_obj = ""
        obj_set.store(['store_obj'])
        load_obj = obj_set.load(['store_obj'])
        obj_set.remove_set()

        assert 'store_obj' in self.shell.user_ns.keys()
        

    def test_persist_mutiple_items(self):
        obj_set = StorageSet(self.shell, 'temp', self.base_dir)
        store_obj = ""        
        store_lambda = lambda x:x
        store_function = mock_function
        
        obj_set.store(['store_obj','store_lambda','store_function'])        
        obj_set.load(['store_obj','store_lambda','store_function'])
        obj_set.remove_set()

        assert 'store_obj' in self.shell.user_ns.keys()
        assert 'store_lambda' in self.shell.user_ns.keys()
        assert 'store_function' in self.shell.user_ns.keys()

    def test_remove_set(self):
        obj_set = StorageSet(self.shell, 'temp', self.base_dir)
        obj_set.remove_set()

        assert 'temp' not in [n for n,s in list_sets(self.base_dir)]

unittest.main()