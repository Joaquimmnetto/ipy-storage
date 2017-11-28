import inspect
import traceback
from termcolor import cprint
from pprint import pprint

def build_suite(suite_members):        
    funcs = {name:obj for name,obj in suite_members}
    
    class suite_ns: pass
    suite_ns.setup = funcs['setup']
    suite_ns.cleanup = funcs['cleanup']
    suite_ns.cleanup_test = funcs['cleanup_test']
    suite_ns.tests = [obj for name,obj in funcs.items() 
                        if (inspect.isfunction(obj) and name.startswith('test'))]
    return suite_ns

def run_tests(suite):    
    test_count = 0
    suite.setup()
    for test in suite.tests:
        try:
            cprint(test.__name__, "yellow")            
            test()            
            cprint("PASS", "green")            
            test_count+=1
        except AssertionError:            
            cprint("FAIL", "red")
            
        suite.cleanup_test()
    suite.cleanup()
    if test_count == len(suite.tests):
        cprint("--------Passed all {} tests--------".format(test_count),'green')
    else:
        cprint("--------Passed {} tests, failed {}--------".format(test_count, len(suite.tests)-test_count),'red')


def ipy_instantiate(*vars, remote_locals):
    ip = get_ipython()    
    for var in vars:
        var_name = [n for n,obj in remote_locals.items() if obj==var][0]
        get_ipython().user_ns[var_name] = var

def ipy_from_userns(*names):
    ip = get_ipython()    
    results = []
    for var in names:        
        results.append(ip.user_ns[var])        
    return tuple(results)