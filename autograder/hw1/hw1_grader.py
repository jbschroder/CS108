import csv
import unittest, sys, os, importlib
from io import StringIO
sys.path.append("..")
import autograder
import matplotlib

# UPDATE:  Homework# here and below (4 total times)
class TestHomework1(unittest.TestCase):

    def __init__(self, test_name, filename):
        super(TestHomework1, self).__init__(test_name)
        self.filename = filename

    ## setUp method is run before each test
    def setUp(self):
        try:
            backup = sys.stdout
            sys.stdout = StringIO()
            if self.filename in sys.modules:
                importlib.reload(sys.modules[ self.filename ] )
            else:
                importlib.import_module( self.filename )
            self.output = sys.stdout.getvalue().strip()
        finally:
            sys.stdout = backup
            
    def test_load(self):
        self.assertTrue(True, msg = "Testing that code loads")

    def test_output(self):
        # UPDATE: can import turtle_generator (download file and import)
        #         can load a turtle from file here, and then run checks
        #         need to end this function with an assert...
        #import pdb; pdb.set_trace()
        self.assertTrue("hello world" in self.output.lower(), msg = "Testing output contains `Hello World`")

if __name__=='__main__':
    # UPDATE: If you add a new test function, you have to add it in the below test_ lists 
    test_names = ['test_load', 'test_output']
    test_points = [50, 50]
    test_feedbacks = ['Cannot load .py file', 'Running .py file does not print Hello World']
    # UPDATE: You need to update homework number in two places below
    autograder.grade_homework(TestHomework1, 1, test_names, test_points, test_feedbacks)
