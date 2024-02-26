import csv
import unittest, sys, os, importlib
from io import StringIO
sys.path.append("..")
import autograder
import matplotlib

# UPDATE:  Homework# here and below (4 total times)
class TestHomework2(unittest.TestCase):

    def __init__(self, test_name, filename):
        super(TestHomework2, self).__init__(test_name)
        self.filename = filename

    ## setUp method is run before each test
    ## this routine executes the student's code (I think?)
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

    def test_turtle_loading(self):
        # UPDATE: can import turtle_generator (download file and import)
        #         can load a turtle from file here, and then run checks
        #         need to end this function with an assert...
        #import pdb; pdb.set_trace()
        
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        self.assertTrue( turtle.nx == 14, msg = "Turtle grid size in x changed from 14")
        self.assertTrue( turtle.ny == 14, msg = "Turtle grid size in y changed from 14")
        self.assertTrue( turtle.start_location == (0,0), msg = "Turtle start location changed from (0,0) ")
        self.assertTrue( turtle.pond_location == (12,12), msg = "Turtle pond location changed from (12,12) ")
        self.assertTrue( turtle.maze_number == 1, msg = "Turtle maze number should be 1")
        self.assertTrue( turtle.number_of_turtles == 1, msg = "There should only be 1 turtle")

        with open(self.filename+".py") as myfile:
            file_contents = myfile.read().lower().replace(' ', '')
            self.assertTrue("turtle=turtle_generator(maze_number=" in file_contents, msg = "Where is the turtle_generator line?") 
            self.assertTrue("turtle.start_new_journey()" in file_contents, msg = "Where is the start_new_journey line?") 
            self.assertTrue("turtle.move_right()" in file_contents, msg = "Where are your move_right lines?") 
            self.assertTrue("turtle.move_up()" in file_contents, msg = "Where are your move_up lines?") 
            self.assertTrue("turtle.check_maze_completed()" in file_contents, msg = "Where is your check_maze_completed line?") 
            if not ("turtle.save_everything_to_file()" in file_contents):
                print ("   " + self.filename + " forgot a save turtle to file line, code may still have correct parts, cannot check")
            self.assertTrue("turtle.save_everything_to_file()" in file_contents, msg = "Where is your save_everything_to_file line?") 
        #
        matplotlib.pyplot.close('all')
        


    def test_turtle_tasks(self):
        #import pdb; pdb.set_trace()
        
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        
        self.assertTrue(turtle.check_maze_completed() == True, msg = "Your turtle did not successfully complete maze, turtle.check_maze_completed() returned False")
        #
        matplotlib.pyplot.close('all')


    def test_cleanup(self):
        # remove turtle file
        import os
        try:
            os.system("rm turtle.pickle") 
            print("removed file..")
        except:
            pass
        #
        matplotlib.pyplot.close('all')

if __name__=='__main__':
    # UPDATE: If you add a new test function, you have to add it in the below test_ lists 
    test_names = ['test_load', 'test_turtle_loading', 'test_turtle_tasks', 'test_cleanup']
    test_points = [15, 65, 20, 0]
    test_feedbacks = ['Cannot load .py file', 'Turtle does not load properly', 'Turtle does not complete maze', 'No turtle file created']
    # UPDATE: You need to update homework number in two places below
    autograder.grade_homework(TestHomework2, 2, test_names, test_points, test_feedbacks)
