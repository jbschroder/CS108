import csv
import unittest, sys, os, importlib
from io import StringIO
sys.path.append("..")
import autograder
import matplotlib

# UPDATE:  Homework# here and below (4 total times)
class TestHomework5(unittest.TestCase):

    def __init__(self, test_name, filename):
        super(TestHomework5, self).__init__(test_name)
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
        
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        #import pdb; pdb.set_trace()
        
        self.assertTrue( turtle.nx == 14, msg = "Turtle grid size in x changed from 14")
        self.assertTrue( turtle.ny == 14, msg = "Turtle grid size in y changed from 14")
        #self.assertTrue( turtle.start_location == (0,0), msg = "Turtle start location changed from (0,0) ")  # This has separate test below
        self.assertTrue( turtle.pond_location == (12,12), msg = "Turtle pond location changed from (12,12) ")
        self.assertTrue( turtle.maze_number == 2, msg = "Turtle maze number should be 2")
        self.assertTrue( turtle.number_of_turtles == 1, msg = "There should be 1 turtle")

        with open(self.filename+".py") as myfile:
            # Make file all lower case, and strip all spaces
            file_contents = myfile.read().lower().replace(' ', '')
            self.assertTrue("=turtle_generator(maze_number=" in file_contents, msg = "Where is the turtle_generator line?") 
            self.assertTrue(".start_new_journey()" in file_contents, msg = "Where is the start_new_journey line?") 
            self.assertTrue(".move_right(" in file_contents, msg = "Where are your move_right lines?") 
            self.assertTrue(".move_up(" in file_contents, msg = "Where are your move_up lines?") 
            #self.assertTrue(".check_maze_completed(" in file_contents, msg = "Where is your check_maze_completed line?") 
            if not (".save_everything_to_file()" in file_contents):
                print ("   " + self.filename + " forgot a save turtle to file line, code may still have correct parts, cannot check")
            self.assertTrue(".save_everything_to_file()" in file_contents, msg = "Where is your save_everything_to_file line?") 
        #
        matplotlib.pyplot.close('all')
        


    def test_turtle_start_loc(self):
        
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        #import pdb; pdb.set_trace()

        # They can either start the turtle at (2,8), or move the turtle there
        correct_start_loc = False
        if turtle.start_location == (2,8):
            correct_start_loc = True
        else:
            moves, trail = turtle.turtles[0].get_movements_and_trail()
            if (2,8) in moves:
                correct_start_loc = True

        self.assertTrue(correct_start_loc , msg = "Turtle start location changed from (2,8) ")
        #
        matplotlib.pyplot.close('all')


    def test_turtle_complete_maze(self):
        #import pdb; pdb.set_trace()
        
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        #import pdb; pdb.set_trace()
        
        self.assertTrue(turtle.check_maze_completed() == True, msg = "Your turtle did not successfully complete maze, turtle.check_maze_completed() returned False")
        #
        matplotlib.pyplot.close('all')
    

    def test_continuous_movements(self):
        import pickle
        filehandler = open('turtle.pickle', 'rb')
        turtle = pickle.load(filehandler)
        #import pdb; pdb.set_trace()
        
        self.assertTrue(turtle.check_continuous_movements() == True , msg = "Turtle movements not continuous ")
        #
        matplotlib.pyplot.close('all')

   # The students implemented setting the starting location to (2,8) in too many different ways, for me
   # to test for a simple REGEX line match like below.  So, I'm commenting this out, and just requiring above, that
   # their turtle visit (2,8)
   #def test_move_turtle_structure(self):
   #    import pickle
   #    import re
   #    filehandler = open('turtle.pickle', 'rb')
   #    turtle = pickle.load(filehandler)
   #    #import pdb; pdb.set_trace()

   #    # they are supposed to call a function named move_turtle with a start_loc parameter.  Make sure that line appears

   #    with open(self.filename+".py") as myfile:
   #        # Make file all lower case, and strip all spaces
   #        file_contents = myfile.read().lower().replace(' ', '')
   #        
   #        # RegEx search for move_turtle command
   #        m = re.search(r'move_turtle\(.*start_loc=\(2,8\).*\)', file_contents)
   #        move_turtle_correct = False
   #        if m is not None:
   #            move_turtle_correct = True
   #        ##
   #        self.assertTrue(move_turtle_correct == True, msg = "move_turtle function doesn't use start_loc") 
   #    #
   #    matplotlib.pyplot.close('all')
        

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
    test_points =    [15,                            15,                            25,                                   25,                      20,                            0]
    test_names =     ['test_load',            'test_turtle_loading',           'test_turtle_start_loc',          'test_turtle_complete_maze', 'test_continuous_movements',  'test_cleanup']
    test_feedbacks = ['Cannot load .py file', 'Turtle does not load properly', 'Turtle does not start at (2,8)', 'Maze not completed',        'turtle moves not continuous', 'No turtle file created']
    # UPDATE: You need to update homework number in two places below
    autograder.grade_homework(TestHomework5, 5, test_names, test_points, test_feedbacks)
