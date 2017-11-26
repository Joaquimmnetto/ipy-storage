import unittest

from dillpickleshare import PickleShareDB
from storage import SetStoreMagics
from IPython import get_ipython


class TestStorage(unittest.TestCase):
    
    def setUp(self):
      self.ip = get_ipython()

    def test_list_sets_default_base(self):
        store = SetStoreMagics(self.ip)

    def test_list_sets_custom_base(self):
        pass

    def test_setopen_default_base(self):
        pass

    def test_setopen_custom_base(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()