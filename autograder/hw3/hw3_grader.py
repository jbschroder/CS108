import csv
import unittest, sys, os, importlib
from io import StringIO
sys.path.append("..")
import autograder

# UPDATE:  Homework# here and below (4 total times)
class TestHomework3(unittest.TestCase):

    def __init__(self, test_name, filename):
        super(TestHomework3, self).__init__(test_name)
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
        self.assertTrue( turtle.number_of_turtles == 2, msg = "There should be 2 turtles")

        with open(self.filename+".py") as myfile:
            # Make file all lower case, and strip all spaces
            file_contents = myfile.read().lower().replace(' ', '')
            self.assertTrue("turtle=turtle_generator(maze_number=" in file_contents, msg = "Where is the turtle_generator line?") 
            self.assertTrue("turtle.start_new_journey()" in file_contents, msg = "Where is the start_new_journey line?") 
            self.assertTrue("turtle.move_right(which_turtle=" in file_contents, msg = "Where are your move_right lines?") 
            self.assertTrue("turtle.move_up(which_turtle=" in file_contents, msg = "Where are your move_up lines?") 
            self.assertTrue("turtle.check_maze_completed(which_turtle=" in file_contents, msg = "Where is your check_maze_completed line?") 
            self.assertTrue("turtle.save_everything_to_file()" in file_contents, msg = "Where is your save_everything_to_file line?") 
        


    def test_turtles_complete_maze(self):
        #import pdb; pdb.set_trace()
        
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        
        self.assertTrue(turtle.check_maze_completed() == True, msg = "Your turtle 0 did not successfully complete maze, turtle.check_maze_completed(which_turtle=0) returned False")
        self.assertTrue(turtle.check_maze_completed() == True, msg = "Your turtle 1 did not successfully complete maze, turtle.check_maze_completed(which_turtle=1) returned False")
    
    def test_alternating_trail(self):
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        
        moves0, trail0 = turtle.turtles[0].get_movements_and_trail()
        moves1, trail1 = turtle.turtles[1].get_movements_and_trail()

        correct_trail0 = [False, True, False, True, False, True, False, True, False, True, False, True, False, \
                            True, False, True, False, True, False, True, False, True, False, True, False]
        correct_trail1 = [False, False, True, False, True, False, True, False, True, False, True, False, True, \
                            False, True, False, True, False, True, False, True, False, True, False, True]
        
        # Allow them to alternate in both ways
        correct_trails = False
        if (trail0 == correct_trail0) and (trail1 == correct_trail1):
            correct_trails = True
        elif (trail0 == correct_trail1) and (trail1 == correct_trail0):
            correct_trails = True

        self.assertTrue(correct_trails == True, msg = "Turtles left an incorrect trail")
        

    def test_cleanup(self):
        # remove turtle file
        import os
        try:
            os.system("rm turtle.pickle") 
            print("removed file..")
        except:
            pass

if __name__=='__main__':
    # UPDATE: If you add a new test function, you have to add it in the below test_ lists 
    test_points =    [15,                            25,                            30,                             30,                            0]
    test_names =     ['test_load',            'test_turtle_loading',           'test_turtles_complete_maze',    'test_alternating_trail',      'test_cleanup']
    test_feedbacks = ['Cannot load .py file', 'Turtle does not load properly', 'Turtle does not complete maze', 'Alternating trail incorrect', 'No turtle file created']
    # UPDATE: You need to update homework number in two places below
    autograder.grade_homework(TestHomework3, 3, test_names, test_points, test_feedbacks)
