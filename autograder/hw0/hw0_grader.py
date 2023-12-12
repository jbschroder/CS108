import csv
import unittest, sys, os, importlib
from io import StringIO
sys.path.append("..")
import autograder

class TestHomework0(unittest.TestCase):

    def __init__(self, test_name, filename):
        super(TestHomework0, self).__init__(test_name)
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
        self.assertTrue("Hello World" in self.output, msg = "Testing output contains `Hello World`")

if __name__=='__main__':
    test_names = ['test_load', 'test_output']
    test_points = [50, 50]
    test_feedbacks = ['Cannot load .py file', 'Running .py file does not print Hello World']
    autograder.grade_homework(TestHomework0, 'hw0_grades.csv', test_names, test_points, test_feedbacks)
